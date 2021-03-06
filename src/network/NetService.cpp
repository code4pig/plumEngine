#include "network/NetService.h"
#include "common/common.h"
#include "common/log.h"
#include "network/NetMessage.h"
#include "network/compressor.h"
#include <string>
#include <chrono>
#include "network/CAsioConnection.h"

namespace network{

	NetService::NetService(asio::io_service& main_io, bool encrypt, uint32 max_clients) :BaseNetService(main_io, encrypt), acceptor_(io_service_), max_clients_(max_clients)
	{ 

	}

	NetService::~NetService()
	{

	}

	bool NetService::init(int32 nettype, t_on_accept_cb accept_cb, t_on_recv_cb recv_cb, t_on_disconnect_cb discon_cb)
	{
		if (BaseNetService::init())
		{
			m_tSvr = nettype;
			on_accept_cb_ = accept_cb;
			on_recvmsg_cb_ = recv_cb;
			on_disconnect_cb_ = discon_cb;
			if (encrypt_)
			{
				LOG_INFO("netserver type %d encrypt is open, max net message compress buf is set to %d", nettype, DEFAULTALLOC);
			}
			else
			{
				LOG_INFO("netserver type %d encrypt is closed", nettype);
			}
			LOG_INFO("netserver type %d max net message len is set to %d", nettype, NetMessage::max_body_length);
			connect_index_ = 1;
			thread_ = std::make_shared<std::thread>(std::thread(
				[this](){
				try{
					io_service_.run();
					ready2shutdown();
				}
				catch (std::exception& e){
					//所有的异常上层都应该自己处理，到这里就无法恢复了，崩掉吧
					LOG_ERROR("netserver type %d net_io_service_ poll Exception: %s\n", m_tSvr, e.what());
					__FooCrash();
				}
			}));
			thread_->detach();
			return true;
		}
		return false;
	}

	bool NetService::start(const char* addr, int32 port, uint16 limit_msg_num, uint8 limit_invalid_num, bool encrypt, int32 maxclients)
	{
		set_max_client(maxclients);
		set_encrypt(encrypt);
		std::string strAddr = addr;
		limit_msg_num_ = limit_msg_num, 
		limit_invalid_num_ = limit_invalid_num;
		io_service_.post([this, strAddr, port]()
		{
			asio::ip::address_v4 address = asio::ip::address_v4::from_string(strAddr.c_str());
			asio::ip::tcp::endpoint endpoint(address, port);
			acceptor_.open(endpoint.protocol());
			//服务端在acceptor开始accept前调用set_option。不需要对单独socket再次set_option。
			//客户端直接对socket set_option
#ifndef _WIN32
			//windows下不要reuse，否则重复绑定不会崩溃，而会去等待
			acceptor_.set_option(asio::ip::tcp::acceptor::reuse_address(true));
#endif
			//acceptor_.set_option(asio::ip::tcp::acceptor::keep_alive(true));
			acceptor_.set_option(asio::ip::tcp::no_delay(true));
			asio::socket_base::send_buffer_size opsz;
			asio::socket_base::receive_buffer_size oprz;
			acceptor_.get_option(opsz);
			acceptor_.get_option(oprz);
			LOG_INFO("netserver type %d send buf size is %d, recv buf size is %d", m_tSvr, opsz.value(), oprz.value());
			acceptor_.bind(endpoint);
			acceptor_.listen();
			LOG_INFO("netserver type %d start server %s:%d\n", m_tSvr, strAddr.c_str(), port);
			do_accept();
		});
		return true;
	}

	std::shared_ptr<AsioConnection> NetService::get_peer(uint32 pid)
	{
		auto it = connections_.find(pid);
		if (it == connections_.end()) {
			return std::shared_ptr<AsioConnection>();
		}
		return it->second;
	}

	bool NetService::send(uint32 pid, t_proto proto_type, const char* msg, size_t msglen)
	{
		if (msglen > NetMessage::max_body_length)
		{
			char msgname[30] = { 0 };
			memcpy(msgname, msg, sizeof(msgname) - 1);
			LOG_ERROR("netserver type %d conn %d send message length exceeded %s %d", m_tSvr, pid, msgname, msglen);
			disconnect(pid);
			return false;
		}
		if (msglen > NetMessage::max_body_length / 2)
		{
			char msgname[30] = { 0 };
			memcpy(msgname, msg, sizeof(msgname) - 1);
			LOG_WARNING("netserver type %d conn %d send large packet to client %s %d", m_tSvr, pid, msgname, msglen);
		}
		std::shared_ptr<std::string> buf = std::make_shared<std::string>(msg, msglen);
		io_service_.post(
			[this, pid, proto_type, buf]()
		{
			do_send(pid, proto_type, buf);
		});
		return true;
	}

	void NetService::disconnect(uint32 pid)
	{
		LOG_INFO("netserver type %d disconnect %d", m_tSvr, pid);
		io_service_.post(
			[this, pid]()
		{
			std::shared_ptr<AsioConnection> conn = get_peer(pid);
			if (conn)
			{
				do_close(*conn);
			}
		});
		return;
	}

	void NetService::shutdown()
	{
		io_service_.post(
			[this]()
		{
			for (auto iter = connections_.begin(); iter != connections_.end(); ++iter)
			{
				iter->second->close();
			}
			connections_.clear();
			BaseNetService::shutdown();
		});
	}

	void NetService::set_max_client(uint32 max_client)
	{
		max_clients_ = max_client;
	}

	uint32 NetService::get_max_client()
	{
		return max_clients_;
	}

	uint32 NetService::get_connection_counts()
	{
		return (uint32)connections_.size();
	}

	int32 NetService::get_service_type()
	{
		return m_tSvr;
	}

	void NetService::CheckHeartBeat()
	{
		io_service_.post(
			[this]()
		{
			//LOG_INFO("CHECK HEART BEART %d", m_tSvr);
			for (auto iter = connections_.begin(); iter != connections_.end();)
			{
				if (iter->second->GetHeartBeatTag() == 0)
				{
					//检测期间未收到心跳包认为断线，断开连接，报告上层
					if (!iter->second->is_connected())
						continue;//不要重复close
					LOG_INFO("netserver type %d need to close %d as heartbeat failed", m_tSvr, iter->first);
					iter->second->close();
					on_disconnect_cb(iter->first);
					connections_.erase(iter++);
				}
				else
				{
					iter->second->SetHeartBeatTag(0);
					iter++;
				}
			}
		});
	}

	/////////////////////////////////
	void NetService::do_accept()
	{
		if (get_state() == ST_RUN)
		{
			if (get_connection_counts() < get_max_client())
			{
				std::shared_ptr<CServerConnection> conn = std::make_shared<CServerConnection>(*this, encrypt_, limit_msg_num_, limit_invalid_num_);
				conn->set_pid(connect_index_++);
				acceptor_.async_accept(conn->get_socket(),
					[this, conn](const asio::error_code& ec)
				{
					//get_peer_ip可能触发异常，捕获处理掉，防止丢给run
					if (!ec && conn->init_peer_ip())
					{
						uint32 pid = conn->get_pid();
						conn->on_connected();
						connections_[pid] = conn;
						std::string &ip = conn->get_peer_ip();
						LOG_INFO("netserver type %d accept pid:%d ip:%s", m_tSvr, pid, ip.c_str());
						on_accept_cb(pid, ip);
						conn->do_read_header();
					}
					do_accept();
				});
			}
			else
			{
				LOG_ERROR("netserver type %d do_accept failed, cur connection count is %d, max connection count is %d", m_tSvr, get_connection_counts(), get_max_client());
			}
		}
		else
		{
			LOG_ERROR("netserver type %d do_accept failed, state is %d", m_tSvr, get_state());
		}
	}

	bool NetService::do_send(uint32 pid, t_proto proto_type, const std::shared_ptr<std::string>& msg)
	{
		std::shared_ptr<AsioConnection> conn = get_peer(pid);
		if (conn)
		{
			conn->send(proto_type, msg);
			return true;
		}
		return false;
	}

	void NetService::do_close(AsioConnection& conn)
	{
		if (!conn.is_connected())
			return;//不要重复close
		LOG_INFO("netserver type %d do_close %d", m_tSvr, conn.get_pid());
		conn.close();
		on_disconnect_cb(conn.get_pid());
		connections_.erase(conn.get_pid());
	}

//////////////////////////////////////////////////////
//丢回主线程执行
	void NetService::on_accept_cb(uint32 pid, std::string ip)
	{
		main_io_service_.post(
			[this, pid, ip]()
		{
			on_accept_cb_(this, pid, ip);
		});
	}

	void NetService::on_disconnect_cb(uint32 pid)
	{
		main_io_service_.post(
			[this, pid]()
		{
			on_disconnect_cb_(this, pid);
		});
	}

	void NetService::on_recvmsg_cb(AsioConnection& conn, t_proto proto_type, std::shared_ptr<std::string> msg)
	{
		if (proto_type == 0)
		{
			//心跳消息自己处理就好
			//LOG_INFO("netserver type %d recv heartbeat %d", m_tSvr, pid);
			conn.OnHeartBeat();
		}
		else
		{
			uint32 pid = conn.get_pid();
			main_io_service_.post(
				[this, pid, proto_type, msg]()
			{
				on_recvmsg_cb_(this, pid, proto_type, msg);
			});
		}
	}

};

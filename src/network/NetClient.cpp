#include "common/log.h"
#include "network/NetClient.h"

namespace network{

	using asio::ip::tcp;

	NetClient::NetClient(asio::io_service& main_io, bool encrypt)
		: BaseNetService(main_io, encrypt)
	{
	}

	NetClient::~NetClient()
	{
	}

	bool NetClient::init(int32 nettype, t_on_connect_cb conn_cb, t_on_connect_fail_cb conn_fail_cb, t_on_recv_cb recv_cb, t_on_disconnect_cb discon_cb)
	{
		if (BaseNetService::init())
		{
			m_tCli = nettype;
			on_connect_cb_ = conn_cb;
			on_connect_fail_cb_ = conn_fail_cb;
			on_recvmsg_cb_ = recv_cb;
			on_disconnect_cb_ = discon_cb;
			if (encrypt_)
			{
				LOG_INFO("netclient type %d encrypt is open, max net message compress buf is set to %d", nettype, DEFAULTALLOC);
			}
			else
			{
				LOG_INFO("netclient type %d encrypt is closed", nettype);
			}
			LOG_INFO("netclient type %d max net message len is set to %d", nettype, NetMessage::max_body_length);
			thread_ = std::make_shared<std::thread>(std::thread(
				[this](){
				try{
					io_service_.run();
					ready2shutdown();
				}
				catch (std::exception& e){
					//所有的异常上层都应该自己处理，到这里就无法恢复了，崩掉吧
					LOG_ERROR("netclient type %d net_io_service_ poll Exception: %s\n", m_tCli, e.what());
					__FooCrash();
				}
			}));
			thread_->detach();
			return true;
		}
		return false;
	}

	bool NetClient::connect(const char* szAddr, int port, bool encrypt, int32 retrytimes, int32 retrysec)
	{
		if (conn_)
		{
			LOG_ERROR("netclient type %d do_connect but already connected %s %d", m_tCli, m_addrStr.c_str(), m_port);
			return false;
		}
		encrypt_ = encrypt;
		m_retrys = retrytimes;
		m_retrysec = retrysec;
		m_addrStr = szAddr;
		m_port = (uint16)port;
		conn_ = std::make_shared<CClientConnection>(*this, encrypt_);
		io_service_.post(
			[this]()
		{
			do_connect();
		});
		return true;
	}

	bool NetClient::send(t_proto proto_type, const char* msg, size_t msglen)
	{
		if (!conn_ || !conn_->is_connected())
		{
			return false;
		}
		if (msglen > NetMessage::max_body_length)
		{
			char msgname[30] = { 0 };
			memcpy(msgname, msg, sizeof(msgname) - 1);
			LOG_ERROR("netclient type %d send message length exceeded %s %d", m_tCli, msgname, msglen);
			disconnect();
			return false;
		}
		if (msglen > NetMessage::max_body_length / 2)
		{
			char msgname[30] = { 0 };
			memcpy(msgname, msg, sizeof(msgname) - 1);
			LOG_WARNING("netclient type %d send large packet to client %s %d", m_tCli, msgname, msglen);
		}
		std::shared_ptr<std::string> buf = std::make_shared<std::string>(msg, msglen);
		io_service_.post(
			[this, proto_type, buf]()
		{
			do_send(proto_type, buf);
		});
		return true;
	}

	bool NetClient::disconnect()
	{
		io_service_.post(
			[this]()
		{
			shutdown();
		});
		return true;
	}

	int32 NetClient::get_client_type()
	{
		return m_tCli;
	}

	int32 NetClient::get_retry_times()
	{
		return m_retrys;
	}

	std::string& NetClient::get_addr_str()
	{
		return m_addrStr;
	}

	uint16 NetClient::get_port()
	{
		return m_port;
	}

	void NetClient::HeartBeat()
	{
		//发送心跳包
		if (conn_ && conn_->is_connected())
		{
			//LOG_INFO("netclient type %d send heartbeat packet", m_tCli);
			send(0, "a", 1);
		}
	}

/////////////////////////////////
	bool NetClient::do_send(t_proto proto_type, const std::shared_ptr<std::string>& msg)
	{
		if (conn_)
		{
			conn_->send(proto_type, msg);
		}
		return true;
	}

	bool NetClient::do_connect()
	{
		if (conn_->connect(m_addrStr, m_port))
		{
			LOG_INFO("netclient type %d do connect to server %s:%d\n", m_tCli, m_addrStr.c_str(), m_port);
			return true;
		}
		m_retrys = 0;//无需重置
		return false;
	}

	void  NetClient::shutdown()
	{
		if (get_state() == ST_DOWN)
		{
			return;
		}
		if (conn_)
		{
			conn_->close();
			on_disconnect_cb();
		}
		BaseNetService::shutdown();
	}

	void  NetClient::do_close(AsioConnection& conn)
	{
		shutdown();
	}

	void NetClient::on_connect_cb(AsioConnection& conn)
	{
		main_io_service_.post(
			[this]()
		{
			on_connect_cb_(this, *conn_);
		});
	}

	void NetClient::on_connect_fail_cb(AsioConnection& conn, std::string errmsg)
	{
		LOG_INFO("netclient type %d on_connect_fail_cb", m_tCli);
		if (m_retrys == 0)
		{
			main_io_service_.post(
				[this, errmsg]()
			{
				on_connect_fail_cb_(this, errmsg);
			});
		}
		else
		{
			LOG_INFO("netclient type %d on_connect_fail_cb but need retry, remain times %d", m_tCli, m_retrys > 0 ? m_retrys-- : m_retrys);
			asio::io_service tmp_service;
			asio::steady_timer timer(tmp_service);
			std::function<void(const asio::error_code&)> tcb = [this, &tmp_service](const asio::error_code& ec)
			{
				//此处触发tick的实际处理
				tmp_service.post(
					[this]()
				{
					conn_->re_connect(m_addrStr, m_port);
				});
			};
			timer.expires_from_now(std::chrono::seconds(m_retrysec));
			timer.async_wait(tcb);
			tmp_service.run();
		}
	}

	void NetClient::on_disconnect_cb()
	{
		main_io_service_.post(
			[this]()
		{
			on_disconnect_cb_(this);
		});
	}

	void NetClient::on_recvmsg_cb(AsioConnection& conn, t_proto proto_type, std::shared_ptr<std::string> msg)
	{
		uint32 pid = conn.get_pid();
		main_io_service_.post(
			[this, pid, proto_type, msg]()
		{
			on_recvmsg_cb_(this, pid, proto_type, msg);
		});
	}

};

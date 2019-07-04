#include "network/CClientConnection.h"
#include "network/BaseNetService.h"
#include "common/log.h"

namespace network
{
	CClientConnection::CClientConnection(BaseNetService& net, bool encrypt) :AsioConnection(net, encrypt)
	{

	}

	CClientConnection::~CClientConnection()
	{

	}

	bool CClientConnection::connect(const std::string& addr, uint16 port)
	{
		//open可能产生异常
		try
		{
			socket_.open(tcp::v4());
			socket_.set_option(tcp::no_delay(true));
			//socket_.set_option(asio::socket_base::keep_alive(true));
			asio::socket_base::send_buffer_size opsz;
			asio::socket_base::receive_buffer_size oprz;
			socket_.get_option(opsz);
			socket_.get_option(oprz);
			LOG_INFO("conn %d send buf size is %d, recv buf size is %d", get_pid(), opsz.value(), oprz.value());
			/*
			socket_.set_option(asio::socket_base::send_buffer_size(16 * 1024));
			socket_.set_option(asio::socket_base::receive_buffer_size(20 * 1024));
			socket_.get_option(opsz);
			socket_.get_option(oprz);
			LOG_INFO("after send buf size is %d, recv buf size is %d", opsz.value(), oprz.value());
			*/
		}
		catch (std::exception& e){
			get_net().on_connect_fail_cb(*this, e.what());
			return false;
		}
		do_connect(addr, port);
		return true;
	}

	void CClientConnection::re_connect(const std::string& addr, uint16 port)
	{
		do_connect(addr, port);
	}

	void CClientConnection::do_connect(const std::string& addr, uint16 port)
	{
		tcp::resolver resolver(get_net().get_ioservice());
		tcp::resolver::iterator endpoint_iterator;
		endpoint_iterator = resolver.resolve(tcp::resolver::query(addr, std::to_string(port)));
		asio::async_connect(socket_, endpoint_iterator,
			[this](const std::error_code& ec, tcp::resolver::iterator iter)
		{
			if (!ec)
			{
				asio::ip::tcp::endpoint real = *iter;
				ip_ = real.address().to_string();
				sendbuf_.clear();
				on_connected();
				get_net().on_connect_cb(*this);
				do_read_header();
			}
			else
			{
				get_net().on_connect_fail_cb(*this, ec.message());
			}
		});
	}

}
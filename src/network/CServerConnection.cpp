#include "network/CServerConnection.h"
#include "common/log.h"

namespace network
{
	CServerConnection::CServerConnection(BaseNetService& net, bool encrypt, uint16 limit_msg_num, uint8 limit_invalid_num) : AsioConnection(net, encrypt)
	{
		limit_msg_num_ = limit_msg_num;
		limit_invalid_num_ = limit_invalid_num;
	}

	CServerConnection::~CServerConnection()
	{

	}

	bool CServerConnection::init_peer_ip()
	{
		asio::error_code ec;
		asio::ip::tcp::endpoint endpoint = socket_.remote_endpoint(ec);
		if (ec)
		{
			LOG_ERROR("get_peer_ip failed err %d, shutdown %d, errmsg %s", ec.value(), get_pid(), ec.message().c_str());
			return false;
		}
		ip_ = endpoint.address().to_string();
		return true;
	}

}
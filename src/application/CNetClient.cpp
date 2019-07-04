#include "application/CNetClient.h"
#include "common/log.h"

namespace application
{
	CNetClient::CNetClient(asio::io_service& main_service)
	{
		m_pNetCli = new NetClient(main_service);
	}

	CNetClient::~CNetClient()
	{
		SAFE_DELETE(m_pNetCli);
	}

	bool CNetClient::Init(int32 nettype, network::NetClient::S_NCB_CLI* p_ncb)
	{
		m_tCli = nettype;
		return (m_pNetCli && m_pNetCli->init(nettype, p_ncb->ccb, p_ncb->cfcb, p_ncb->rcb, p_ncb->dcb));
	}

	bool CNetClient::Connect(const char* szAddr, int32 port, bool encrypt, int32 retrytimes, int32 retrysec)
	{
		return m_pNetCli && m_pNetCli->connect(szAddr, port, encrypt, retrytimes, retrysec);
	}

	bool CNetClient::Close()
	{
		if (m_pNetCli)
		{
			m_pNetCli->shutdown();
			return true;
		}
		return false;
	}

	bool CNetClient::Send(t_proto proto_type, const char* msg, size_t msglen)
	{
		return m_pNetCli->send(proto_type, msg, msglen);
	}

	void CNetClient::HeartBeat()
	{
		m_pNetCli->HeartBeat();
	}

}
#include "application/CMtApplication.h"
#include "script/PyThreadStateLock.h"
#include "common/log.h"

using namespace common;

namespace application
{
	CMtApplication::CMtApplication()
	{

	}

	CMtApplication::~CMtApplication()
	{

	}

	void CMtApplication::InitScript(const char* szModuleName)
	{
		PyEval_InitThreads();
		LOG_INFO("%s", "open py thread support");
		CApplication::InitScript(szModuleName);
		PyEval_ReleaseThread(PyThreadState_Get());
	}

	void CMtApplication::StartScript()
	{
		script::PyThreadStateLock pylock;
		CApplication::StartScript();
	}

	void CMtApplication::UnInitScript()
	{
		script::PyThreadStateLock pylock;
		CApplication::UnInitScript();
	}

	void CMtApplication::OnUpdate()
	{
		script::PyThreadStateLock pylock;
		CApplication::OnUpdate();
	}

	void mt_connect_cb(NetService* ns, uint32 pid, std::string ip)
	{
		script::PyThreadStateLock pylock;
		connect_cb(ns, pid, ip);
	}

	void  mt_recv_cb(NetService* ns, uint32 pid, t_proto proto_type, std::shared_ptr<std::string> msg)
	{
		script::PyThreadStateLock pylock;
		recv_cb(ns, pid, proto_type, msg);
	}

	void  mt_disconnect_cb(NetService* ns, uint32 pid)
	{
		script::PyThreadStateLock pylock;
		disconnect_cb(ns, pid);
	}

	void CMtApplication::InitNcb()
	{
		m_pNcb->acb = mt_connect_cb;
		m_pNcb->rcb = mt_recv_cb;
		m_pNcb->dcb = mt_disconnect_cb;
	}

	void  mt_connect_cb_cli(NetClient* nc, AsioConnection& conn)
	{
		script::PyThreadStateLock pylock;
		connect_cb_cli(nc, conn);
	}

	void  mt_connect_fail_cb_cli(NetClient* nc, std::string msg)
	{
		script::PyThreadStateLock pylock;
		connect_fail_cb_cli(nc, msg);
	}

	void  mt_recv_cb_cli(NetClient* nc, uint32 pid, t_proto proto_type, std::shared_ptr<std::string> msg)
	{
		script::PyThreadStateLock pylock;
		recv_cb_cli(nc, pid, proto_type, msg);
	}

	void  mt_disconnect_cb_cli(NetClient* nc)
	{
		script::PyThreadStateLock pylock;
		disconnect_cb_cli(nc);
	}

	void CMtApplication::InitNcbClient()
	{
		m_pNcb_Cli->ccb = mt_connect_cb_cli;
		m_pNcb_Cli->cfcb = mt_connect_fail_cb_cli;
		m_pNcb_Cli->rcb = mt_recv_cb_cli;
		m_pNcb_Cli->dcb = mt_disconnect_cb_cli;
	}

}

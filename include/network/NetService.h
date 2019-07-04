/*
Copyright (C) 2017, Zhang Baofeng.

BSD 2-Clause License (http://www.opensource.org/licenses/bsd-license.php)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

You can contact the author via email : zhangbaofeng@joygame.cc
This is the NetServer service based on asio's io_service and uses one thread to deal with
network events.
*/

#pragma once
#include "common/common.h"
#include <thread>
#include "asio/asio.hpp"
#include <memory>
#include "BaseNetService.h"
#include "CServerConnection.h"

namespace network{

	using asio::ip::tcp;
	using namespace common;

	class NetService :public BaseNetService
	{
	public:
		
		typedef std::function<void(NetService*, uint32, std::string)> t_on_accept_cb;
		typedef std::function<void(NetService*, uint32, t_proto, std::shared_ptr<std::string>)> t_on_recv_cb;
		typedef std::function<void(NetService*, uint32)> t_on_disconnect_cb;

		typedef struct {
			t_on_accept_cb acb;
			t_on_recv_cb rcb;
			t_on_disconnect_cb dcb;
		}S_NCB;

		NetService(asio::io_service& main_io, bool encrypt = false, uint32 max_clients = 5000);
		virtual ~NetService();

		virtual bool init(int32 nettype, t_on_accept_cb accept_cb, t_on_recv_cb recv_cb, t_on_disconnect_cb discon_cb);
		bool start(const char* addr, int32 port, uint16 limit_msg_num, uint8 limit_invalid_num, bool encrypt, int32 maxclients);
		virtual void shutdown();
		virtual void do_close(AsioConnection& conn);
		virtual void on_recvmsg_cb(AsioConnection& conn, t_proto proto_type, std::shared_ptr<std::string> msg);

		bool send(uint32 pid, t_proto proto_type, const char* msg, size_t msglen);
		void disconnect(uint32 pid);

		void set_max_client(uint32 max_client);
		uint32 get_max_client();
		uint32 get_connection_counts();
		int32 get_service_type();
		void CheckHeartBeat();

	private:
		void do_accept();
		bool do_send(uint32 pid, t_proto proto_type, const std::shared_ptr<std::string>& msg);
		std::shared_ptr<AsioConnection> get_peer(uint32 pid);
		void on_accept_cb(uint32 pid, std::string ip);
		void on_disconnect_cb(uint32 pid);

	private:
		std::unordered_map<uint32, std::shared_ptr<CServerConnection> > connections_;
		tcp::acceptor acceptor_;
		uint32 connect_index_;
		uint32 max_clients_;
		t_on_accept_cb on_accept_cb_;
		t_on_recv_cb on_recvmsg_cb_;
		t_on_disconnect_cb on_disconnect_cb_;
		int32 m_tSvr;

		uint16 limit_msg_num_;
		uint8 limit_invalid_num_;
	};

};
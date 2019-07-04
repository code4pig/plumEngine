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
This is BaseNetService class.
*/

#pragma once
#include "common/common.h"
#include "asio/asio.hpp"
#include "common/CBaseService.h"

using namespace common;

namespace network{

	class AsioConnection;

	class BaseNetService:public common::CBaseService
	{
	public:
		BaseNetService(asio::io_service& main_io, bool encrypt = false) :main_io_service_(main_io), encrypt_(encrypt){};
		virtual ~BaseNetService(){};

		virtual void do_close(AsioConnection& conn){ };
		virtual void on_recvmsg_cb(AsioConnection& conn, t_proto proto_type, std::shared_ptr<std::string> msg) = 0;
		virtual void on_connect_cb(AsioConnection& conn){};
		virtual void on_connect_fail_cb(AsioConnection& conn, std::string errmsg){};
		asio::io_service& get_main_ioservice(){ return main_io_service_; };
		bool is_encrypt(){ return encrypt_; };
		void set_encrypt(bool encrypt){ encrypt_ = encrypt; }

	protected:
		asio::io_service& main_io_service_;
		bool encrypt_;
	};

};
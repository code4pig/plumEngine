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
This is base network connection class which really handles socket functions.
*/

#pragma once
#include "common/common.h"
#include "asio/asio.hpp"
#include "NetMessage.h"
#include "compressor.h"

#ifdef _DEBUG
#define SERVER_DEBUG
#endif

namespace network{

	using asio::ip::tcp;
	using namespace common;

	class BaseNetService;

	class AsioConnection : public std::enable_shared_from_this<AsioConnection>
	{
	public:
		AsioConnection(BaseNetService& net, bool encrypt);
		virtual ~AsioConnection();
		uint32 get_pid();
		std::string& get_peer_ip();

		BaseNetService& get_net();

		NetMessage& get_read_buffer();
		Lz4Compressor& get_z();
		tcp::socket& get_socket();
		bool is_encrypt();
		bool is_connected();
		void set_pid(uint32 pid);
		bool send(t_proto proto_type, const std::shared_ptr<std::string>& buf);
		bool recv(const std::shared_ptr<std::string>& buf);
		bool close();
		void on_connected();
		void do_read_header();
		void OnHeartBeat();
		uint8 GetHeartBeatTag();
		uint8 SetHeartBeatTag(uint8 newTag);
		bool is_need_msg_num_checker();

	protected:
		void do_write();
		void do_read_body();

		void add_msg_counter();

	protected:
		BaseNetService& net_;
		tcp::socket socket_;
		NetMessage read_msg_;
		std::string sendbuf_;
		Lz4Compressor* pz_;
		std::string ip_;
		uint32 pid_;
		bool encrypt_;
		bool is_connected_;
		bool write_in_progress_;
		uint8 heart_beat_tag_;

		uint16 limit_msg_num_; 
		uint8 limit_invalid_num_;
		int64 last_check_timestamp_;
		int64 last_invalid_timestamp_;
		uint32 msg_count_;	// 定时器间隔时间内消息数量
		uint8 invalid_count_;	// 非法次数

#ifdef SERVER_DEBUG
		int nAskSend;
		int nRealSend;
		int nRawRecv;
		int nDecomRecv;
#endif
	};

};


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
This is the base asio service.
*/

#pragma once
#include <thread>
#include <mutex>
#include "common/common.h"
#include "asio/asio.hpp"

namespace common{

	class CBaseService
	{
	public:

		typedef enum{
			ST_INIT = 0,
			ST_RUN,
			ST_PREPARE2DOWN,
			ST_READY2DOWN,
			ST_DOWN,
		}SERVICE_STATE;

	public:
		CBaseService() :work_(std::make_shared<asio::io_service::work>(io_service_)), state_(ST_INIT){};
		virtual ~CBaseService(){};

		virtual bool init()
		{
			if (get_state() == ST_INIT)
			{
				set_state(ST_RUN);
				return true;
			}
			return false;
		};
		virtual void prepare_shutdown(){ set_state(ST_PREPARE2DOWN); };
		virtual void ready2shutdown(){ set_state(ST_READY2DOWN); };
		virtual void shutdown(){ set_state(ST_DOWN); io_service_.stop(); };
		asio::io_service& get_ioservice(){ return io_service_; };

		SERVICE_STATE get_state(){ std::lock_guard<std::mutex> lck(m_mutex); return state_; };
		void set_state(SERVICE_STATE st){ std::lock_guard<std::mutex> lck(m_mutex); state_ = st; };

		virtual const std::thread::id get_threadid()const{ return thread_->get_id(); }

	protected:
		std::mutex	m_mutex;
		asio::io_service io_service_;
		std::shared_ptr<std::thread> thread_;
		std::shared_ptr<asio::io_service::work> work_;
		SERVICE_STATE state_;
	};

};
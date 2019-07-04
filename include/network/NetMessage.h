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
This is the netmessage class with prototype+bodylen+body.
*/

#pragma once
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include "common/commdef.h"
#include "common/log.h"

namespace network{

	using namespace common;

	class NetMessage
	{
	public:
		static const uint8 header_length = sizeof(uint8) + sizeof(uint32);
		static const uint32 max_body_length = 1024 * 256;

		NetMessage()
			: body_length_(0)
		{
			memset(data_, 0, header_length + max_body_length);
		}

		const char* data() const
		{
			return data_;
		}

		char* data()
		{
			return data_;
		}

		uint32 length() const
		{
			return header_length + body_length_;
		}

		const char* body() const
		{
			return data_ + header_length;
		}

		char* body()
		{
			return data_ + header_length;
		}

		uint32 body_length() const
		{
			return body_length_;
		}

		bool body_length(uint32 new_length)
		{
			if (new_length > max_body_length || new_length == 0)
			{
				LOG_ERROR("ERROR!!! message length %d\n", new_length);
				return false;
			}
			body_length_ = new_length;
			return true;
		}

		bool decode_header()
		{
			return body_length(*(uint32*)(data_ + 1));
		}

		void encode_header(t_proto proto_type)
		{
			data_[0] = (unsigned char)proto_type;
			memcpy(data_ + 1, (const void*)(&body_length_), sizeof(uint32));
		}

		t_proto get_prototype()
		{
			return (t_proto)data_[0];
		}

	private:
		uint32 body_length_;
		char data_[header_length + max_body_length];
	};

};

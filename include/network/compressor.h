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
This is the stream compressor which uses lz4 algorithm, it can be used as encrypter and compressor both.
*/

#pragma once
#include <sstream>
#include <memory>
#include "lz4.h"
#include "NetMessage.h"

namespace network{

	using namespace common;

	/* The output buffer will be increased in chunks of DEFAULTALLOC bytes. */
	#define DEFAULTALLOC (NetMessage::max_body_length * 2)

	class BaseCompressor
	{
	public:
		virtual ~BaseCompressor(){};

		virtual void reflesh() = 0;

		virtual int compress(std::string& out_data, const std::string& in_data) = 0;
		virtual int uncompress(std::string& out_data, const std::string& in_data) = 0;
	};

	//lz4
	class Lz4CompressObj
	{
	public:
		Lz4CompressObj();
		~Lz4CompressObj();
		int compress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data);
		void reset();
	private:
		int m_inpOffset;
		LZ4_stream_t* m_pStream;
		char m_ringBuf[DEFAULTALLOC];
		char m_outBuf[LZ4_COMPRESSBOUND(NetMessage::max_body_length)];
	};

	class Lz4DeCompressObj
	{
	public:
		Lz4DeCompressObj();
		~Lz4DeCompressObj();
		int decompress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data);
		void reset();
	private:
		int   m_decOffset;
		LZ4_streamDecode_t* m_pStream;
		char m_ringBuf[DEFAULTALLOC];
		char m_outBuf[NetMessage::max_body_length];
	};

	class Lz4Compressor
	{
	public:
		Lz4Compressor();
		~Lz4Compressor();
		void reflesh();
		int compress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data);
		int uncompress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data);
	private:
		Lz4CompressObj m_com;
		Lz4DeCompressObj m_decom;

	};

};

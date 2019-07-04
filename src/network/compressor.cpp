#include "network/compressor.h"
#include <cstring>

namespace network{

	Lz4CompressObj::Lz4CompressObj()
	{
		m_pStream = LZ4_createStream();
		reset();
	}

	Lz4CompressObj::~Lz4CompressObj()
	{
		if (m_pStream)
			LZ4_freeStream(m_pStream);
	}

	void Lz4CompressObj::reset()
	{
		LZ4_resetStream(m_pStream);
		memset(m_ringBuf, 0, sizeof(m_ringBuf));
		memset(m_outBuf, 0, sizeof(m_outBuf));
		m_inpOffset = 0;
	}

	int Lz4CompressObj::compress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data)
	{
		size_t inpBytes = in_data->size();
		if (inpBytes > NetMessage::max_body_length)
			return 0;//超过长度直接不发送，上层最好断开连接
		if (m_inpOffset >= DEFAULTALLOC - NetMessage::max_body_length)
			m_inpOffset = 0;//ring buf
		char* const inpPtr = &m_ringBuf[m_inpOffset];
		memcpy(inpPtr, in_data->c_str(), inpBytes);
		const int cmpBytes = LZ4_compress_continue(m_pStream, inpPtr, m_outBuf, (int)inpBytes);
		if (cmpBytes <= 0)
			return 0;
		m_inpOffset += (int)inpBytes;
		out_data->assign(m_outBuf, cmpBytes);
		return cmpBytes;
	}

	Lz4DeCompressObj::Lz4DeCompressObj() :m_decOffset(0)
	{
		m_pStream = LZ4_createStreamDecode();
		reset();
	}

	Lz4DeCompressObj::~Lz4DeCompressObj()
	{
		if (m_pStream)
			LZ4_freeStreamDecode(m_pStream);
	}

	void Lz4DeCompressObj::reset()
	{
		memset(m_pStream, 0, sizeof(LZ4_streamDecode_t));
		memset(m_ringBuf, 0, sizeof(m_ringBuf));
		memset(m_outBuf, 0, sizeof(m_outBuf));
		m_decOffset = 0;
	}

	int Lz4DeCompressObj::decompress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data)
	{
		size_t cmpBytes = in_data->size();
		uint32 boundSize = LZ4_COMPRESSBOUND(NetMessage::max_body_length);
		if (cmpBytes >= boundSize)
			return 0;//超过最大长度直接不处理，上层应该断开连接
		if (m_decOffset >= DEFAULTALLOC - NetMessage::max_body_length)
			m_decOffset = 0;
		char* const decPtr = &m_ringBuf[m_decOffset];
		const int decBytes = LZ4_decompress_safe_continue(
			m_pStream, in_data->c_str(), decPtr, (int)cmpBytes, NetMessage::max_body_length);
		if (decBytes <= 0)
			return 0;
		memcpy(m_outBuf, decPtr, decBytes);
		m_decOffset += decBytes;
		out_data->assign(m_outBuf, decBytes);
		return decBytes;
	}

	Lz4Compressor::Lz4Compressor()
	{

	}

	Lz4Compressor::~Lz4Compressor()
	{

	}

	void Lz4Compressor::reflesh()
	{
		m_com.reset();
		m_decom.reset();
	}

	int Lz4Compressor::compress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data)
	{
		return m_com.compress(out_data, in_data);
	}

	int Lz4Compressor::uncompress(const std::shared_ptr<std::string>& out_data, const std::shared_ptr<std::string>& in_data)
	{
		return m_decom.decompress(out_data, in_data);
	}

};

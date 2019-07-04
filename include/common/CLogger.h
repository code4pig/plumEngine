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
This is the real logger module base on log4cplus, it will run in the same thread with the caller.
*/

#pragma once
#include "common.h"
#include "logdef.h"
#include <mutex>
#include <log4cplus/logger.h>

namespace common{

	class CLogger
	{
	private:
		CLogger(const char *pszLogDir, const char *pszAppName);
		virtual ~CLogger(void);

		static CLogger *sm_pLogger;
		static char g_scriptCache[4096*2];
	public:
		static void CreateLogger(const char *pszLogDir, const char *pszAppName);
		static void DestroyLogger(void);
		static CLogger*	Instance(void) { return sm_pLogger; }

	public:
		void SetLogLevel(LogLevel logLv);
		bool IsEnabledLevel(LogLevel logLv);
		LogLevel GetLogLevel();
		const std::string& GetLogDir();
		void Log(LogLevel logLv, const char *pszMsg);
		void LogMod(LogLevel logLv, const char* pszMsg, const char* szMod = ENGINE_MOD);
		void ScriptCache(const char* szCache);
		void ScriptFlush(LogLevel logLv);
	protected:
		log4cplus::Logger& GetInnerLogger(const char* szName);
		void UpdateAppender(log4cplus::Logger& logger);
		bool BeforeLogMod(LogLevel logLv, const char* szMod);

		int LogLv2Log4cplusLogLv(LogLevel lv)
		{
			switch (lv)
			{
			case LOG_LV_TRACE:		return log4cplus::TRACE_LOG_LEVEL;
			case LOG_LV_DEBUG:		return log4cplus::DEBUG_LOG_LEVEL;
			case LOG_LV_INFO:		return log4cplus::INFO_LOG_LEVEL;
			case LOG_LV_WARNING:	return log4cplus::WARN_LOG_LEVEL;
			case LOG_LV_ERROR:		return log4cplus::ERROR_LOG_LEVEL;
			case LOG_LV_FATAL:		return log4cplus::FATAL_LOG_LEVEL;
			}
			return 0;
		}

	private:
		typedef std::map<std::string, log4cplus::Logger> t_loggermap;
		std::mutex m_mutex;
		t_loggermap m_loggerMap;
		LogLevel m_nLogLevel;

		std::string m_strLogDir;
		std::string m_strAppName;
		uint64 m_uDayNum;
	};

};

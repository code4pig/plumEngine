#include <stdio.h>
#ifdef _WIN32
#include <io.h>
#include <Windows.h>
#define snprintf _snprintf
#else
#include <unistd.h>
#include <sys/stat.h>
#endif
#include "common/CLogger.h"
#include "common/CTime.h"
#include <thread>
#include <log4cplus/consoleappender.h>
#include <log4cplus/fileappender.h>
#include <log4cplus/layout.h>
#include <log4cplus/loggingmacros.h>
#include <log4cplus/asyncappender.h>

namespace common{

	//#define _USE_ASYNC_LOG
#define LAYEROUT "[%D{%Y-%m-%d-%H-%M-%S}],%p,%m"//"%D	%p	%m%n"
#define CONSOLE_LAYER "[%D{%Y-%m-%d-%H-%M-%S}],%p,%m"//"%D[%p] %m%n"

#define MAX_LOGFILE_SIZE	0x7fffffff

#define TODAY_NUM	((GetFastUTCTimeInSec() + 28800) / 86400)

#ifndef min
#define min(a,b)            (((a) < (b)) ? (a) : (b))
#endif

	CLogger* CLogger::sm_pLogger = NULL;
	char CLogger::g_scriptCache[4096*2] = { 0 };

	CLogger::CLogger(const char *pszLogDir, const char *pszAppName)
		:m_strLogDir(pszLogDir)
		, m_strAppName(pszAppName)
	{
#ifdef _WIN32
		if (_access(pszLogDir, 0) == -1)
#else
		if (access(pszLogDir, 0) == -1)
#endif
		{
#ifdef _WIN32
			if (!::CreateDirectory(pszLogDir, NULL))
				__FooCrash();
#else
			if (mkdir(pszLogDir, 0777) != 0)
				__FooCrash();
#endif
		}
		GetInnerLogger(ENGINE_MOD);
		SetLogLevel(LOG_LV_TRACE);
	}

	CLogger::~CLogger()
	{

	}

	void CLogger::CreateLogger(const char *pszLogDir, const char *pszAppName)
	{
		if (NULL == sm_pLogger)
		{
			sm_pLogger = new CLogger(pszLogDir, pszAppName);
		}
	}

	void CLogger::DestroyLogger()
	{
		if (sm_pLogger)
		{
			delete sm_pLogger;
			sm_pLogger = 0;
		}
	}

	LogLevel CLogger::GetLogLevel()
	{
		return m_nLogLevel;
	}

	const std::string& CLogger::GetLogDir()
	{
		return m_strLogDir;
	}

	log4cplus::Logger& CLogger::GetInnerLogger(const char* szName)
	{
		if (m_loggerMap.find(szName) == m_loggerMap.end())
		{
			m_loggerMap[szName] = log4cplus::Logger::getInstance(szName);
			UpdateAppender(m_loggerMap[szName]);
		}
		return m_loggerMap[szName];
	}

	void CLogger::SetLogLevel(LogLevel logLv)
	{
		m_nLogLevel = logLv;
		log4cplus::LogLevel lv = LogLv2Log4cplusLogLv(logLv);
		for (auto iter = m_loggerMap.begin(); iter != m_loggerMap.end(); iter++)
		{
			iter->second.setLogLevel(lv);
		}
	}

	bool CLogger::IsEnabledLevel(LogLevel logLv)
	{
		return (logLv >= m_nLogLevel);
	}


	void CLogger::Log(LogLevel logLv, const char *pszMsg)
	{
		LogMod(logLv, pszMsg);
	}

	void CLogger::ScriptCache(const char* szCache)
	{
		//只需要写入缓冲区即可
		memcpy(g_scriptCache + strlen(g_scriptCache), szCache, min(sizeof(g_scriptCache) - strlen(g_scriptCache) - 1, strlen(szCache)));
		//snprintf(g_scriptCache + strlen(g_scriptCache), min(sizeof(g_scriptCache) - strlen(g_scriptCache) - 1, strlen(szCache)), szCache);
		*(g_scriptCache + strlen(g_scriptCache)) = 0;
	}

	bool CLogger::BeforeLogMod(LogLevel logLv, const char* szMod)
	{
		LOG4CPLUS_SUPPRESS_DOWHILE_WARNING()
		log4cplus::LogLevel lv = LogLv2Log4cplusLogLv(logLv);
		log4cplus::Logger curLogger = GetInnerLogger(szMod);
		if (!curLogger.isEnabledFor(lv))
		{
			return false;
		}
		if (TODAY_NUM != m_uDayNum)
		{
			//这里要up所有的appender
			for (auto iter = m_loggerMap.begin(); iter != m_loggerMap.end(); ++iter)
			{
				UpdateAppender(iter->second);
			}
		}
		return true;
	}

	void CLogger::ScriptFlush(LogLevel logLv)
	{
		std::lock_guard<std::mutex> lck(m_mutex);
		if (BeforeLogMod(logLv, "script"))
		{
			log4cplus::Logger curLogger = GetInnerLogger("script");
			LOG4CPLUS_SUPPRESS_DOWHILE_WARNING()
			log4cplus::LogLevel lv = LogLv2Log4cplusLogLv(logLv);
			LOG4CPLUS_MACRO_INSTANTIATE_OSTRINGSTREAM(_log4cplus_buf);

			if (g_scriptCache[0])
			{
				_log4cplus_buf << std::this_thread::get_id() << "," << g_scriptCache << "\n";
				memset(g_scriptCache, 0, sizeof(g_scriptCache));
			}
			log4cplus::detail::macro_forced_log(curLogger, lv, _log4cplus_buf.str(),
				__FILE__, __LINE__, LOG4CPLUS_MACRO_FUNCTION());
			LOG4CPLUS_RESTORE_DOWHILE_WARNING()
		}
	}

	void CLogger::LogMod(LogLevel logLv, const char* pszMsg, const char* szMod)
	{
		std::lock_guard<std::mutex> lck(m_mutex);
		if (BeforeLogMod(logLv, szMod))
		{
			log4cplus::Logger curLogger = GetInnerLogger(szMod);
			LOG4CPLUS_SUPPRESS_DOWHILE_WARNING()
			log4cplus::LogLevel lv = LogLv2Log4cplusLogLv(logLv);
			LOG4CPLUS_MACRO_INSTANTIATE_OSTRINGSTREAM(_log4cplus_buf);
			_log4cplus_buf << std::this_thread::get_id() << "," << pszMsg << "\n";
			log4cplus::detail::macro_forced_log(curLogger, lv, _log4cplus_buf.str(),
				__FILE__, __LINE__, LOG4CPLUS_MACRO_FUNCTION());
			LOG4CPLUS_RESTORE_DOWHILE_WARNING()
		}
	}

	void CLogger::UpdateAppender(log4cplus::Logger& logger)
	{
		m_uDayNum = TODAY_NUM;
		time_t now = time(NULL);
		tm t = *std::localtime(&now);
		char szDirName[2048] = { 0 };
		snprintf(szDirName, sizeof(szDirName) - 1, "%s/%s_%d%02d%02d", m_strLogDir.c_str(), m_strAppName.c_str(), t.tm_year + 1900, t.tm_mon + 1, t.tm_mday);
#ifdef _WIN32
		if (_access(szDirName, 0) == -1)
#else
		if (access(szDirName, 0) == -1)
#endif
		{
#ifdef _WIN32
			if (!::CreateDirectory(szDirName, NULL))
			{
				__FooCrash();
			}
#else
			if (mkdir(szDirName, 0777) != 0)
				__FooCrash();
#endif
		}
		char szFileName[4096] = { 0 };
		logger.removeAllAppenders();
		memset(szFileName, 0, sizeof(szFileName));
		snprintf(szFileName, sizeof(szFileName) - 1, "%s/%s.log", szDirName, logger.getName().c_str());

		log4cplus::helpers::SharedObjectPtr<log4cplus::Appender> appender(new log4cplus::RollingFileAppender(szFileName, MAX_LOGFILE_SIZE, 10, true));
		std::auto_ptr<log4cplus::Layout> layout(new log4cplus::PatternLayout(LAYEROUT));
		appender->setLayout(layout);

#ifdef _USE_ASYNC_LOG
		log4cplus::helpers::SharedObjectPtr<log4cplus::Appender> async_appender(new log4cplus::AsyncAppender(appender, 1024));
		logger.addAppender(async_appender);
#else
		logger.addAppender(appender);
#endif

#ifdef _WIN32
		log4cplus::helpers::SharedObjectPtr<log4cplus::Appender> console_appender(new log4cplus::ConsoleAppender);
		std::auto_ptr<log4cplus::Layout> console_layout(new log4cplus::PatternLayout(CONSOLE_LAYER));
		console_appender->setLayout(console_layout);
		logger.addAppender(console_appender);
#endif
	}

};

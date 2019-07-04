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
This is the exported log functions and defines.
*/

#pragma once
#include "logdef.h"
#include "commdef.h"

namespace common{

	#ifdef __cplusplus
		extern "C"{
	#endif
			PLUMAPI void InitLogger(const char *pszLogDir, const char *pszAppName);
			PLUMAPI void UninitLogger(void);

			PLUMAPI void SetLogLevel(LogLevel logLv);
			PLUMAPI int	IsEnabledLogLevel(LogLevel logLv);

			PLUMAPI void Log(LogLevel uLevel, const char* szFormat, ...);
			PLUMAPI void LogScriptCache(const char* szFormat, ...);
			PLUMAPI void LogScriptFlush();
			PLUMAPI void LogMod(LogLevel uLevel, const char* szMod, const char* szFormat, ...);
			PLUMAPI void Log_NoFormat(LogLevel uLevel, const char *pszMsg, const char* pszMod);
			PLUMAPI int	MyPrintf(const char *format, ...);
	#ifdef __cplusplus
		}
	#endif

	#ifndef LOG_TRACE
	#define LOG_TRACE(fmt, ...) do{Log(LOG_LV_TRACE, fmt, __VA_ARGS__);}while(0)
	#endif

	#ifndef LOG_DEBUG
	#define LOG_DEBUG(fmt, ...) do{Log(LOG_LV_DEBUG, fmt, __VA_ARGS__);}while(0)
	#endif

	#ifndef LOG_INFO
	#define LOG_INFO(fmt, ...) do{Log(LOG_LV_INFO, fmt, __VA_ARGS__);}while(0)
	#endif

	#ifndef LOG_WARNING
	#define LOG_WARNING(fmt, ...) do{Log(LOG_LV_WARNING, fmt, __VA_ARGS__);}while(0)
	#endif

	#ifndef LOG_ERROR
	#define LOG_ERROR(fmt, ...) do{Log(LOG_LV_ERROR, fmt, __VA_ARGS__);}while(0)
	#endif

	#ifndef LOG_FATAL
	#define LOG_FATAL(fmt, ...) do{Log(LOG_LV_FATAL, fmt, __VA_ARGS__);}while(0)
	#endif

	#ifndef LOG_INFO_NOFMT
	#define LOG_INFO_NOFMT(msg) do{Log_NoFormat(LOG_LV_INFO, msg, ENGINE_MOD);}while(0)
	#endif

	#ifndef LOG_MOD_NOFMT
	#define LOG_MOD_NOFMT(mod, msg) do{Log_NoFormat(LOG_LV_INFO, msg, mod);}while(0)
	#endif

	#ifndef PRINTF
	#define PRINTF(fmt, ...) do{Log(LOG_LV_INFO, fmt, __VA_ARGS__);}while(0)
	#endif

	#ifndef LOG_SCRIPT_CACHE
	#define LOG_SCRIPT_CACHE(fmt, ...) do{LogScriptCache(fmt, __VA_ARGS__);}while(0)
	#endif
	#ifndef LOG_SCRIPT_FLUSH
	#define LOG_SCRIPT_FLUSH() do{LogScriptFlush();}while(0)
	#endif


};
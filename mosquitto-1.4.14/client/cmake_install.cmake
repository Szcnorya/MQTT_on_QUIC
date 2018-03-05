# Install script for directory: /Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/client

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/client/mosquitto_pub")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_pub" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_pub")
    execute_process(COMMAND "/usr/bin/install_name_tool"
      -change "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/lib/libmosquitto.1.dylib" "libmosquitto.1.dylib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_pub")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_pub")
    execute_process(COMMAND /usr/bin/install_name_tool
      -add_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_pub")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_pub")
    endif()
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/client/mosquitto_sub")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_sub" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_sub")
    execute_process(COMMAND "/usr/bin/install_name_tool"
      -change "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/lib/libmosquitto.1.dylib" "libmosquitto.1.dylib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_sub")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_sub")
    execute_process(COMMAND /usr/bin/install_name_tool
      -add_rpath "/usr/local/lib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_sub")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/mosquitto_sub")
    endif()
  endif()
endif()


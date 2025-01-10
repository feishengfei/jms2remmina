# JMS 2 Remmina

Redirect [JumpServer](https://github.com/jumpserver/jumpserver)   **jms://** URI to [remmina](https://gitlab.com/Remmina/Remmina) client.

There is no linux rdp client for jumpserver, so this application provide workaround:

step 01: parse client information from '**jms://**' URI;
step 02: compose temp '.remmina' config from usr, host info;
step 03: invoke 'remmina' to setup rdp connection to remote host.



You may also refer to official JumpServer client.

https://github.com/jumpserver/clients



# Demo


Select 'Connect Type' to **RDP Client** before click **Confirm**.

![](img/select__RDP_Client__before__Confirm.png)

Click **Open JMS2Remmina** to invoke 'remmina' to setup rdp connection to remote host.

![](img/select__JMS2Remmina__to_start_up_remmina_for_rdp_connection.png)



# Settings

About how to change default behavior of remmina, just edit following templete.

 `/usr/share/jms2remmina.remmina`

## resolution

Below is the definition of resolution_mode used by remmina.

``` c
typedef enum {
    RES_INVALID         = -1, 
    RES_USE_CUSTOM          = 0,
    RES_USE_CLIENT          = 1,
    RES_USE_INITIAL_WINDOW_SIZE = 2 
} RemminaProtocolWidgetResolutionMode;
```

| resolution_mode | Meaning                                                      |
| --------------- | ------------------------------------------------------------ |
| 0               | you have to setup both **resolution_width** & **resolution_height**. |
| 1               | use the same resolution as client.                           |
| 2               | default value, which may mean a very limited scope.          |





# Limitation

password is not presented in URI, so you may need to re-type password in login session window.

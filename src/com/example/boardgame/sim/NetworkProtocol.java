package com.example.boardgame.sim;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;

public class NetworkProtocol {
	HttpClient httpclient = new DefaultHttpClient();
	
	public NetworkProtocol() {
	
	  HttpPost post = new HttpPost("http");
	  
	//HttpResponse response = httpclient.execute(new HttpPo);
	}
}

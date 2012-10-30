package com.example.boardgame.sim;

import java.util.LinkedList;
import java.util.List;

import com.example.boardgame.sim.PlayingTable.Item;

import android.graphics.*;

public class PlayingTable {
	public class Item {
		private Bitmap image;
		Rect size;
		Rect position;
		boolean movable;
		public Item () {
			image = null;
			size = new Rect(0,0,0,0);
			position = new Rect(0,0,0,0); 
			movable = false;
		}
		public Item (Bitmap b, Rect size, Rect position, boolean movable) {
			this.image = b;
			this.size = size;
			this.position = position;
			this.movable = movable;
		}
		
		public void setImage(Bitmap image) {
			this.image = image;
		}
		
		public Bitmap getImage() {
			return this.image;
		}
		
		public void setSize(Rect size) {
			this.size = size;
		}
		
		public Rect getSize() {
			return this.size;
		}
		
		public void setPosition(Rect position) {
			this.position = position;
		}
		
		public Rect getPosition(){
			return this.position;
		}
		
		public boolean isMovable() {
			return this.movable;
		}
		
		public void setMovable() {
			this.setMovable(true);
		}
		
		public void setMovable(boolean movable) {
			this.movable = movable;
		}
	}

	
	private List<Item> Objects = null;
	
	public PlayingTable() {
		Objects = new LinkedList<Item>();
	}
	
	public void add(Bitmap b, Rect size, Rect position, boolean movable) {
		Objects.add(new Item(b,size,position,movable));
	}

	public List<Item> getObjects() {
		return this.Objects;
	}
	
}

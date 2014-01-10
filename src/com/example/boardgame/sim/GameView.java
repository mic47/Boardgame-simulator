package com.example.boardgame.sim;

import java.util.List;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.os.Handler;
import android.os.Message;
import android.util.AttributeSet;
import android.util.Log;
import android.view.*;

public class GameView extends View {

	private Bitmap b;
	private Rect src, dst;
	private final Paint mPaint = new Paint();
	private int x = 0;
	private int y = 0;
	private int dx = 3 + 5;
	private int dy = 1 + 5;
	private boolean drag = false;
	private PlayingTable table = null;

	private RefreshHandler mRedrawHandler = new RefreshHandler();

	class RefreshHandler extends Handler {

		@Override
		public void handleMessage(Message msg) {
			// GameView.this.update();
			GameView.this.invalidate();
		}

		public void sleep(long delayMillis) {
			this.removeMessages(0);
			sendMessageDelayed(obtainMessage(0), delayMillis);
		}
	};

	/**
	 * Constructs a SnakeView based on inflation from XML
	 * 
	 * @param context
	 * @param attrs
	 */
	public GameView(Context context, AttributeSet attrs) {
		super(context, attrs);
		initGameView();
	}

	public GameView(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
		initGameView();
	}

	public GameView(Context context) {
		super(context);
		initGameView();
	}

	private void initGameView() {
		table = new PlayingTable();
		for (int i=0; i<10;i++) {
			b = Bitmap.createBitmap(100, 100, Bitmap.Config.ARGB_8888);
			b.eraseColor(-(int)(Math.random()*16777216+1));
			src = new Rect(0, 0, 100, 100);
			dst = new Rect(src);
			dst.offsetTo((int)(Math.random()*500), (int)(Math.random()*1000));
			table.add(b, src, dst, true);
		}
		
	}

	@Override
	protected void onDraw(Canvas canvas) {

		List<PlayingTable.Item> Items = table.getObjects();

		for (PlayingTable.Item i : Items) {
			canvas.drawBitmap(i.getImage(), i.getSize(), i.getPosition(),
					mPaint);
		}

		mRedrawHandler.sleep(10);
	}

	@Override
	public boolean onTouchEvent(MotionEvent event) {
		// TODO: multi touch
		final int pointerCount = event.getPointerCount();
		if (pointerCount < 1)
			return false;

		List<PlayingTable.Item> Items = table.getObjects();

		for (int pp = 0; pp < pointerCount; pp++) {
			int x = (int) event.getX(pp);
			int y = (int) event.getY(pp);
			for (PlayingTable.Item i : Items) {
		
				if (!i.isMovable()) {
					continue;
				}
				if (i.getPosition().contains(x, y)) {
					Rect p = new Rect(i.getSize());
					p.set(p.left + x - p.width() / 2, p.top + y - p.height()
							/ 2, p.right + x - p.width() / 2,
							p.bottom + y - p.height() / 2);
					i.setPosition(p);
					break;
				}
			}
		}
		return true;
	}

}

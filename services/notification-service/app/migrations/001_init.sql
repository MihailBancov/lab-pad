CREATE TABLE IF NOT EXISTS notifications (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  order_id INTEGER NOT NULL,
  channel VARCHAR(32) NOT NULL DEFAULT 'email',
  message TEXT NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'queued',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS ix_notifications_order_id ON notifications(order_id);

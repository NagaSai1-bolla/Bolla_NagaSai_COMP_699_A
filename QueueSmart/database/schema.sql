-- ==============================
-- USERS TABLE (Patient, Staff, Admin)
-- ==============================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('patient','staff','admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================
-- SERVICE DESKS (OPD, Lab, Pharmacy)
-- ==============================
CREATE TABLE IF NOT EXISTS service_desks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    desk_type TEXT NOT NULL,
    is_open INTEGER DEFAULT 0,
    assigned_staff_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_staff_id) REFERENCES users(id)
);

-- ==============================
-- QUEUES (ONE PER DESK)
-- ==============================
CREATE TABLE IF NOT EXISTS queues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    desk_id INTEGER NOT NULL,
    current_size INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (desk_id) REFERENCES service_desks(id)
);

-- ==============================
-- QUEUE ENTRIES (PATIENT FLOW)
-- ==============================
CREATE TABLE IF NOT EXISTS queue_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    queue_id INTEGER,
    position INTEGER,
    status TEXT DEFAULT 'waiting' 
        CHECK(status IN ('waiting','completed','cancelled')),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (queue_id) REFERENCES queues(id)
);

-- ==============================
-- SERVICE LOGS (STAFF PERFORMANCE)
-- ==============================
CREATE TABLE IF NOT EXISTS service_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER,
    desk_id INTEGER,
    service_time REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (staff_id) REFERENCES users(id),
    FOREIGN KEY (desk_id) REFERENCES service_desks(id)
);

-- ==============================
-- NOTIFICATIONS
-- ==============================
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ==============================
-- INDEXES (PERFORMANCE BOOST)
-- ==============================
CREATE INDEX IF NOT EXISTS idx_queue_user 
ON queue_entries(user_id);

CREATE INDEX IF NOT EXISTS idx_queue_status 
ON queue_entries(status);

CREATE INDEX IF NOT EXISTS idx_service_logs_desk 
ON service_logs(desk_id);
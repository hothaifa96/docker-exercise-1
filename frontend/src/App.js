import React, { useState, useEffect, useCallback } from 'react';

const API = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const styles = {
  app: {
    minHeight: '100vh',
    background: 'var(--bg)',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    padding: '24px 32px 20px',
    borderBottom: '1px solid var(--border)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '16px',
    flexWrap: 'wrap',
    background: 'var(--surface)',
  },
  logo: {
    fontFamily: "'Space Mono', monospace",
    fontSize: '22px',
    fontWeight: '700',
    color: 'var(--accent)',
    letterSpacing: '-0.5px',
  },
  logoSub: {
    fontSize: '11px',
    color: 'var(--text-muted)',
    fontFamily: "'Space Mono', monospace",
    marginTop: '2px',
  },
  searchWrap: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    flex: 1,
    maxWidth: '400px',
  },
  searchInput: {
    flex: 1,
    padding: '9px 14px',
    background: 'var(--surface2)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    color: 'var(--text)',
    fontFamily: "'Syne', sans-serif",
    fontSize: '14px',
    outline: 'none',
    transition: 'border-color 0.2s',
  },
  btnPrimary: {
    padding: '9px 18px',
    background: 'var(--accent)',
    color: '#0f0f0f',
    border: 'none',
    borderRadius: 'var(--radius)',
    fontFamily: "'Syne', sans-serif",
    fontWeight: '700',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'opacity 0.2s, transform 0.1s',
    whiteSpace: 'nowrap',
  },
  main: {
    display: 'flex',
    flex: 1,
    gap: '0',
  },
  sidebar: {
    width: '320px',
    minWidth: '280px',
    borderRight: '1px solid var(--border)',
    overflowY: 'auto',
    background: 'var(--surface)',
    display: 'flex',
    flexDirection: 'column',
  },
  sidebarHeader: {
    padding: '16px 20px 12px',
    fontSize: '11px',
    fontFamily: "'Space Mono', monospace",
    color: 'var(--text-muted)',
    textTransform: 'uppercase',
    letterSpacing: '1.5px',
    borderBottom: '1px solid var(--border)',
  },
  noteItem: (active) => ({
    padding: '16px 20px',
    borderBottom: '1px solid var(--border)',
    cursor: 'pointer',
    background: active ? 'var(--surface2)' : 'transparent',
    borderLeft: active ? '3px solid var(--accent)' : '3px solid transparent',
    transition: 'background 0.15s',
  }),
  noteItemTitle: {
    fontSize: '15px',
    fontWeight: '600',
    color: 'var(--text)',
    marginBottom: '4px',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  noteItemMeta: {
    fontSize: '11px',
    fontFamily: "'Space Mono', monospace",
    color: 'var(--text-muted)',
  },
  noteItemPreview: {
    fontSize: '12px',
    color: 'var(--text-muted)',
    marginTop: '4px',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  editor: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    padding: '32px',
    gap: '16px',
    overflowY: 'auto',
  },
  editorTitle: {
    width: '100%',
    background: 'transparent',
    border: 'none',
    borderBottom: '2px solid var(--border)',
    color: 'var(--text)',
    fontFamily: "'Syne', sans-serif",
    fontWeight: '800',
    fontSize: '28px',
    outline: 'none',
    padding: '8px 0',
    transition: 'border-color 0.2s',
  },
  editorContent: {
    flex: 1,
    width: '100%',
    minHeight: '300px',
    background: 'var(--surface)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    color: 'var(--text)',
    fontFamily: "'Space Mono', monospace",
    fontSize: '14px',
    lineHeight: '1.7',
    padding: '20px',
    outline: 'none',
    resize: 'none',
    transition: 'border-color 0.2s',
  },
  editorActions: {
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
  },
  btnDanger: {
    padding: '9px 18px',
    background: 'transparent',
    color: 'var(--danger)',
    border: '1px solid var(--danger)',
    borderRadius: 'var(--radius)',
    fontFamily: "'Syne', sans-serif",
    fontWeight: '600',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'background 0.2s',
  },
  btnSecondary: {
    padding: '9px 18px',
    background: 'transparent',
    color: 'var(--text-muted)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius)',
    fontFamily: "'Syne', sans-serif",
    fontWeight: '600',
    fontSize: '14px',
    cursor: 'pointer',
  },
  emptyState: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'var(--text-muted)',
    gap: '12px',
    fontFamily: "'Space Mono', monospace",
  },
  emptyIcon: {
    fontSize: '48px',
    opacity: 0.3,
  },
  toast: (type) => ({
    position: 'fixed',
    bottom: '24px',
    right: '24px',
    padding: '12px 20px',
    borderRadius: 'var(--radius)',
    background: type === 'error' ? 'var(--danger)' : '#2a7a4b',
    color: '#fff',
    fontFamily: "'Space Mono', monospace",
    fontSize: '13px',
    zIndex: 1000,
    boxShadow: '0 4px 20px rgba(0,0,0,0.4)',
  }),
  noNotes: {
    padding: '32px 20px',
    color: 'var(--text-muted)',
    fontFamily: "'Space Mono', monospace",
    fontSize: '12px',
    textAlign: 'center',
  },
};

function formatDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

export default function App() {
  const [notes, setNotes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');
  const [search, setSearch] = useState('');
  const [isNew, setIsNew] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 2800);
  };

  const fetchNotes = useCallback(async (q = '') => {
    try {
      const res = await fetch(`${API}/notes${q ? `?search=${encodeURIComponent(q)}` : ''}`);
      const data = await res.json();
      setNotes(data);
    } catch {
      showToast('Cannot reach backend. Check your API URL.', 'error');
    }
  }, []);

  useEffect(() => { fetchNotes(); }, [fetchNotes]);

  useEffect(() => {
    const t = setTimeout(() => fetchNotes(search), 300);
    return () => clearTimeout(t);
  }, [search, fetchNotes]);

  const selectNote = (note) => {
    setSelected(note);
    setEditTitle(note.title);
    setEditContent(note.content || '');
    setIsNew(false);
  };

  const startNew = () => {
    setSelected(null);
    setEditTitle('');
    setEditContent('');
    setIsNew(true);
  };

  const saveNote = async () => {
    if (!editTitle.trim()) { showToast('Title cannot be empty.', 'error'); return; }
    setLoading(true);
    try {
      if (isNew) {
        const res = await fetch(`${API}/notes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: editTitle, content: editContent }),
        });
        const note = await res.json();
        if (!res.ok) throw new Error(note.error);
        await fetchNotes(search);
        setIsNew(false);
        setSelected(note);
        showToast('Note created!');
      } else {
        const res = await fetch(`${API}/notes/${selected.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: editTitle, content: editContent }),
        });
        const note = await res.json();
        if (!res.ok) throw new Error(note.error);
        await fetchNotes(search);
        setSelected({ ...selected, title: editTitle, content: editContent });
        showToast('Note saved!');
      }
    } catch (e) {
      showToast(e.message || 'Error saving note.', 'error');
    }
    setLoading(false);
  };

  const deleteNote = async () => {
    if (!selected) return;
    if (!window.confirm(`Delete "${selected.title}"?`)) return;
    try {
      await fetch(`${API}/notes/${selected.id}`, { method: 'DELETE' });
      await fetchNotes(search);
      setSelected(null);
      setEditTitle('');
      setEditContent('');
      setIsNew(false);
      showToast('Note deleted.');
    } catch {
      showToast('Error deleting note.', 'error');
    }
  };

  const cancelEdit = () => {
    if (isNew) { setIsNew(false); setEditTitle(''); setEditContent(''); }
    else if (selected) { setEditTitle(selected.title); setEditContent(selected.content || ''); }
  };

  const showEditor = isNew || selected;

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <div>
          <div style={styles.logo}>📓 NotesApp</div>
          <div style={styles.logoSub}>Docker Practice Lab</div>
        </div>
        <div style={styles.searchWrap}>
          <input
            style={styles.searchInput}
            placeholder="Search by title..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            onFocus={e => e.target.style.borderColor = 'var(--accent)'}
            onBlur={e => e.target.style.borderColor = 'var(--border)'}
          />
        </div>
        <button style={styles.btnPrimary} onClick={startNew}
          onMouseEnter={e => e.target.style.opacity = '0.85'}
          onMouseLeave={e => e.target.style.opacity = '1'}
        >+ New Note</button>
      </header>

      <div style={styles.main}>
        <aside style={styles.sidebar}>
          <div style={styles.sidebarHeader}>
            {notes.length} note{notes.length !== 1 ? 's' : ''}
            {search && ` · "${search}"`}
          </div>
          {notes.length === 0 && (
            <div style={styles.noNotes}>No notes found.<br />Create one!</div>
          )}
          {notes.map(note => (
            <div
              key={note.id}
              style={styles.noteItem(selected && selected.id === note.id && !isNew)}
              onClick={() => selectNote(note)}
            >
              <div style={styles.noteItemTitle}>{note.title}</div>
              <div style={styles.noteItemMeta}>{formatDate(note.updated_at)}</div>
              {note.content && (
                <div style={styles.noteItemPreview}>{note.content.slice(0, 80)}</div>
              )}
            </div>
          ))}
        </aside>

        <main style={styles.editor}>
          {showEditor ? (
            <>
              <input
                style={styles.editorTitle}
                placeholder="Note title..."
                value={editTitle}
                onChange={e => setEditTitle(e.target.value)}
                onFocus={e => e.target.style.borderColor = 'var(--accent)'}
                onBlur={e => e.target.style.borderColor = 'var(--border)'}
              />
              <textarea
                style={styles.editorContent}
                placeholder="Write your note here..."
                value={editContent}
                onChange={e => setEditContent(e.target.value)}
                onFocus={e => e.target.style.borderColor = 'var(--accent)'}
                onBlur={e => e.target.style.borderColor = 'var(--border)'}
              />
              <div style={styles.editorActions}>
                <button
                  style={styles.btnPrimary}
                  onClick={saveNote}
                  disabled={loading}
                  onMouseEnter={e => e.target.style.opacity = '0.85'}
                  onMouseLeave={e => e.target.style.opacity = '1'}
                >
                  {loading ? 'Saving...' : isNew ? 'Create Note' : 'Save Changes'}
                </button>
                <button style={styles.btnSecondary} onClick={cancelEdit}>Cancel</button>
                {!isNew && selected && (
                  <button
                    style={styles.btnDanger}
                    onClick={deleteNote}
                    onMouseEnter={e => { e.target.style.background = 'var(--danger)'; e.target.style.color = '#fff'; }}
                    onMouseLeave={e => { e.target.style.background = 'transparent'; e.target.style.color = 'var(--danger)'; }}
                  >Delete</button>
                )}
              </div>
            </>
          ) : (
            <div style={styles.emptyState}>
              <div style={styles.emptyIcon}>📝</div>
              <div>Select a note or create a new one</div>
            </div>
          )}
        </main>
      </div>

      {toast && <div style={styles.toast(toast.type)}>{toast.msg}</div>}
    </div>
  );
}

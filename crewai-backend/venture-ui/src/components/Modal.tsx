import React, { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Modal({
  open, onClose, title, children
}: { open: boolean, onClose: () => void, title: string, children: React.ReactNode }) {
  useEffect(() => {
    const onEsc = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    document.addEventListener('keydown', onEsc)
    return () => document.removeEventListener('keydown', onEsc)
  }, [onClose])

  return (
    <AnimatePresence>
      {open && (
        <motion.div className="fixed inset-0 z-50 flex items-center justify-center"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
          <div className="absolute inset-0 bg-black/60" onClick={onClose} />
          <motion.div
            className="card w-[92vw] max-w-3xl max-h-[85vh] overflow-auto p-6 relative"
            initial={{ y: 60, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 60, opacity: 0 }}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold">{title}</h3>
              <button className="pill hover:bg-white/10" onClick={onClose}>Close</button>
            </div>
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

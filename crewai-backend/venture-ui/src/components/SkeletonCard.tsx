export default function SkeletonCard() {
  return (
    <div className="card p-5 animate-pulse">
      <div className="h-5 w-48 bg-white/10 rounded mb-3" />
      <div className="h-3 w-64 bg-white/10 rounded mb-2" />
      <div className="h-3 w-72 bg-white/10 rounded mb-2" />
      <div className="h-3 w-56 bg-white/10 rounded mb-4" />
      <div className="h-6 w-24 bg-white/10 rounded" />
    </div>
  )
}

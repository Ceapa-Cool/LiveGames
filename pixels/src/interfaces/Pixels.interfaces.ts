interface Snapshot {
  pixels: Pixel[][],
  top_placers: User[]
}
interface Pixel {
  color: string,
  placer: User,
  timestamp: number
}
interface User {
  username: string,
  id: string,
  placed: number
}

export type { Snapshot, Pixel, User };

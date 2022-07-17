export class WifiRequest {
  username: string;
  start_time: number;
  duration_in_min: number;
  constructor(username: string, startTime: number, duration_in_min: number) {
    this.username = username;
    this.start_time = startTime;
    this.duration_in_min = duration_in_min;
  }
}

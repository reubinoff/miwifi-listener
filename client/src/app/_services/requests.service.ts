import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { WifiRequest } from '../_models/WifiRequest.model';

const API_URL = 'https://func.listener.reubinoff.com/api/miwifi_scheduler';

@Injectable({
  providedIn: 'root',
})
export class RequestService {
  constructor(private http: HttpClient) {}

  sendRequest(req: WifiRequest): Observable<any> {
    return this.http.post(API_URL, req, { responseType: 'text' });
  }

}
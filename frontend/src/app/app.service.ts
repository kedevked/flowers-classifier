import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  baseUrl = 'http://localhost:5000/';
  constructor(private httpClient: HttpClient) { }

  predict(file) {
   const formData = new FormData();
   formData.append('file', file);

    return this.httpClient.post(`${this.baseUrl}predict`, formData);
  }

}

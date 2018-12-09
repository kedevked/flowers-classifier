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

  uploadModel(modelArchitecture: { arch: any; layers: any[]; }, file: any): any {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('model', JSON.stringify(modelArchitecture));

    return this.httpClient.post(`${this.baseUrl}upload-model`, formData);
  }

}

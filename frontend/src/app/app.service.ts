import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  baseUrl = 'http://localhost:5000/';
  constructor(private httpClient: HttpClient) { }

  predict(file, modelId ?: string) {
   const formData = new FormData();
   formData.append('file', file);
   if (modelId) {
     formData.append('id', modelId);
   }
   const requestUrl = modelId ? 'model_predict' : 'predict';
    return this.httpClient.post(`${this.baseUrl}${requestUrl}`, formData);
  }

  uploadModel(modelArchitecture: { arch: any; layers: any[]; }, file: any, email ?: string): any {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('model', JSON.stringify(modelArchitecture));
    if (email) {
      formData.append('email', email);
    }
    return this.httpClient.post(`${this.baseUrl}upload-model`, formData);
  }

}

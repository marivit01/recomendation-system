import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ProbabilityPrediction } from '../models/prediction';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL = 'http://localhost:8081/api/';

  constructor(private http: HttpClient) {
  }

  public predictStudentPerformance(parameters): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      this.http.post(`${this.API_URL}predict`, parameters).toPromise().then(res => {
        console.log(res);
        resolve(res);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

}

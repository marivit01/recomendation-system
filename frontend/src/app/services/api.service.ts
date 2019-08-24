import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL = 'http://localhost:8081/api/';

  constructor(private http: HttpClient) {
  }

  // private static _handleError(err: HttpErrorResponse | any) {
  //   return Observable.throw(err.message || 'Error: Unable to complete request.');
  // }

  // // GET list of public, future events
  // getExams(): Observable<Exam[]> {
  //   return this.http
  //     .get(`${this.API_URL}/exams`)
  //     .catch(ApiService._handleError);
  // }

//   public trainModel(svcParameters: SVCParameters): Observable<SVCResult> {
//     return this.http.post(`${this.API_URL}train`, svcParameters).map((res) => res.json());
// }
}

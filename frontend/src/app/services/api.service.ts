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

  public predictStudentPerformance(id, target): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      this.http.post(`${this.API_URL}predict-model-2/${id}`, target).toPromise().then(res => {
        console.log('get result', res);
        resolve(res);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

  public predictIndice(id, target): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      this.http.post(`${this.API_URL}predict-model-3/${id}`, target).toPromise().then(res => {
        console.log('get result', res);
        resolve(res);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

  public getAvailableSubjects(studentId): Promise<{code: string, name: string, disabled: boolean}[]> {
    return new Promise<{code: string, name: string, disabled: boolean}[]>((resolve, reject) => {
      this.http.post(`${this.API_URL}getSubjects/${studentId}`, '').toPromise().then(res => {
        console.log(res);
        resolve(res as {code: string, name: string, disabled: boolean}[]);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

  public predictStudentPerformanceByAssigns(id, target): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      this.http.post(`${this.API_URL}predict-model-4/${id}`, target).toPromise().then(res => {
        console.log('get result', res);
        resolve(res);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

  public predictPerformanceModel4_V1(id, target): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      this.http.post(`${this.API_URL}predict-model-4-V1/${id}`, target).toPromise().then(res => {
        console.log('get result', res);
        resolve(res);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

  public predictPerformanceModel5(id, target): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      const quarters = [target, target];
      console.log('quarters', quarters);
      this.http.post(`${this.API_URL}predict-model-5/${id}`, quarters).toPromise().then(res => {
        console.log('get result', res);
        resolve(res);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

}

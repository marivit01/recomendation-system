import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ProbabilityPrediction } from '../models/prediction';
import { PredictionModelFive } from '../models/prediction-model-five';

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

  public predictPerformanceModel5(id, target, unique?:boolean): Promise<PredictionModelFive[]> {
    return new Promise<any>((resolve, reject) => {
      var quarters;
      if(unique) {
        quarters = [target];
      } else {
        quarters = target;
      }
      console.log('quarters', quarters);
      this.http.post(`${this.API_URL}predict-model/${id}`, quarters).toPromise().then(res => {
        console.log('get result', res);
        resolve(res as PredictionModelFive);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

  /** 
   * Funcion para obtener todas las combinaciones de materias posibles
   * para posteriormente predecir sus resectivos rendimientos */
  public getCombinations(availables, preselected, assignsNumber?): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      this.http.post(`${this.API_URL}getCombinations/${assignsNumber}`, {availables, preselected}).toPromise().then(res => {
        console.log('get combinaciones: ', res);
        resolve(res);
      }).catch(err => {
        console.error( 'Error: Unable to complete request.', err);
        reject();
      });
    });
  }

}

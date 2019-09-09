import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { Location } from '@angular/common';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-selection',
  templateUrl: './selection.component.html',
  styleUrls: ['./selection.component.scss']
})
export class SelectionComponent implements OnInit {
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;
  success = false;
  predictionResult;
  studentId: any;
  loading = false;
  loadingPred: boolean;
  resetList = false;
  predictionOption: string;

  constructor(private apiService: ApiService,
    private formBuilder: FormBuilder,
    private location: Location,
    private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.params.subscribe(param => {
      this.predictionOption = param.selection;
      console.log(this.predictionOption);
      this.createForms();
    });
  }

  createForms() {
    this.firstFormGroup = this.formBuilder.group({
      id: ['', Validators.required]
    });
    this.secondFormGroup = this.formBuilder.group({
      targetSubjects: ['', Validators.required]
    });
  }

  nextStep(step) {
    console.log(step);
    switch (step) {
      case 1:
        this.loading = true;
        console.log(step, this.firstFormGroup.value);
        this.studentId = this.firstFormGroup.value.id;
        break;
      case 2:
        this.loadingPred = true;
        this.predict();
        break;
    }
  }

  loaded(event) {
    console.log(event);
    this.loading = event;
  }

  saveSelection(event) {
    console.log(event);
    console.log(this.secondFormGroup.value.targetSubjects);
    this.secondFormGroup.setValue({ targetSubjects: event });
    console.log(this.secondFormGroup.value.targetSubjects);
  }

  goBack() {
    this.location.back();
  }

  predict() {
    const targetQuarter = this.secondFormGroup.value.targetSubjects;
    switch (this.predictionOption) {
      case 'global': {
        console.log('entro en global');
        this.apiService.predictStudentPerformance(this.studentId, targetQuarter).then(res => {
          console.log('res', res);
          this.predictionResult = res[0][0];
          console.log(this.predictionResult);
          if (this.predictionResult >= 0.5) {
            this.success = true;
          } else {
            this.success = false;
          }
          this.loadingPred = false;
          this.apiService.predictIndice(this.studentId, targetQuarter).then(res2 => {
            console.log('Respuesta modelo indice:', res2);
          });
        });
        break;
      }
      case 'custom': {
        console.log('entro en custom');
        this.apiService.predictStudentPerformanceByAssigns(this.studentId, targetQuarter).then(res => {
          console.log('res', res);
          this.predictionResult = res[0][0];
          console.log(this.predictionResult);
          if (this.predictionResult >= 0.5) {
            this.success = true;
          } else {
            this.success = false;
          }
          this.loadingPred = false;
        });
      }
    }
  }

  reset() {
    this.secondFormGroup.reset();
    this.resetList = true;
  }

}

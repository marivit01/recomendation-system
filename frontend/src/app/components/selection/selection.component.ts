import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { Location } from '@angular/common';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-selection',
  templateUrl: './selection.component.html',
  styleUrls: ['./selection.component.css']
})
export class SelectionComponent implements OnInit {
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;
  success = false;
  predictionResult;

  constructor(private apiService: ApiService, private formBuilder: FormBuilder, private location: Location) {}

  ngOnInit() {
    this.createForms();
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
    console.log(step, this.firstFormGroup.value);
    this.secondFormGroup.reset();
  }

  saveSelection(event) {
    console.log(event);
    console.log(this.secondFormGroup.value.targetSubjects);
    this.secondFormGroup.setValue({targetSubjects: event});
    console.log(this.secondFormGroup.value.targetSubjects);
  }

  goBack() {
    this.location.back()
  }

  predict() {
    const studentId = this.firstFormGroup.value.id;
    const targetQuarter = this.secondFormGroup.value.targetSubjects;
    this.apiService.predictStudentPerformance(studentId, targetQuarter).then(res => {
      console.log('res', res);

      this.predictionResult = res;
    });
  }

}

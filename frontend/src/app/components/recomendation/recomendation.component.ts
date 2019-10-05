import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-recomendation',
  templateUrl: './recomendation.component.html',
  styleUrls: ['./recomendation.component.css']
})
export class RecomendationComponent implements OnInit {
  dataForm: FormGroup;
  secondFormGroup: FormGroup;

  allSubjects: { code: string; name: string; disabled: boolean; }[];
  allCombinations = [];
  loading = false;
  studentId: string;
  numberAssigns: string;
  predictionResult;
  loadingPred = false;
  success = false;
  availablesFiltered: { code: string; name: string; disabled: boolean; }[];

  constructor(
    private formBuilder: FormBuilder,
    private apiService: ApiService,
    private route: ActivatedRoute
  ) { }

  ngOnInit() {
    this.createForm();
  }

  createForm() {
    this.dataForm = this.formBuilder.group({
      id: ['', Validators.required],
      numberAssigns: ['']
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
        console.log(step, this.dataForm.value);
        this.studentId = this.dataForm.value.id;
        this.numberAssigns = this.dataForm.value.numberAssigns;
        if (this.numberAssigns === "") {
          this.numberAssigns = 'all';
        }
        break;
      case 2:
        this.loadingPred = true;
        // this.predict();
        this.getCombinations();
        break;
    }
  }

  getAvailablesFiltered(filtered) {
    // this.availablesFiltered = filtered;
    this.secondFormGroup.setValue({ targetSubjects: filtered });

  }

  /**
   * @param availablesFiltered
   * @param number 
   * Funcion que genera todas las posibles combinaciones de materias a partir de
   * el array de las materias disponibles escogidas por el usuario
   */
  getCombinations() {
    this.availablesFiltered = this.secondFormGroup.value.targetSubjects;
    this.apiService.getCombinations(this.availablesFiltered, this.numberAssigns).then(res => {
      // console.log('res', res);
      this.allCombinations = res;
      console.log("all subjects combinations", this.allCombinations);
      this.predict();
    });
  }

  predict() {
    // const targetQuarter = this.secondFormGroup.value.targetSubjects;
    this.apiService.predictPerformanceModel5(this.studentId, this.allCombinations).then(res => {
      console.log('res', res);
      this.predictionResult = res;
      // console.log(this.predictionResult);
      // if (this.predictionResult >= 0.5) {
      //   this.success = true;
      // } else {
      //   this.success = false;
      // }
      this.loadingPred = false;
    });
  }

  loaded(event) {
    console.log(event);
    this.loading = event;
  }

}

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
  allSubjects: { code: string; name: string; disabled: boolean; }[];
  allCombinations = [];
  loading = false;
  studentId: string;
  numberAssigns: string;
  predictionResult;
  loadingPred: boolean;
  success = false;
  predictionOption: string;

  constructor(
    private formBuilder: FormBuilder,
    private apiService: ApiService,
    private route: ActivatedRoute
  ) { }

  ngOnInit() {
    this.createForm();
    this.route.params.subscribe(param => {
      this.predictionOption = param.selection;
      console.log(this.predictionOption);
    });
  }

  createForm() {
    this.dataForm = this.formBuilder.group({
      id: ['', Validators.required],
      numberAssigns: ['']
    });
  }

  nextStep(step) {
    console.log(step);
    switch (step) {
      case 1:
        // if (this.studentId !== this.firstFormGroup.value.id) {
        this.loading = true;
        console.log(step, this.dataForm.value);
        this.studentId = this.dataForm.value.id;
        this.numberAssigns = this.dataForm.value.numberAssigns;
        if (this.numberAssigns === "") {
          this.numberAssigns = 'all';
        }
        this.getAvailableSubjects(this.studentId);
        break;
      //}
    }
  }

  getAvailableSubjects(id) {
    this.apiService.getAvailableSubjects(id).then(res => {
      console.log('res', res);
      this.allSubjects = res.filter(r => {
        if (!r.disabled) {
          return r;
        }
        return null;
      });
      console.log("all subjects", this.allSubjects);
      this.getCombinations(this.numberAssigns);
    });
  }

  getCombinations(number?) {
    this.apiService.getCombinations(this.allSubjects, number).then(res => {
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
      this.predictionResult = res[0][0];
      // console.log(this.predictionResult);
      if (this.predictionResult >= 0.5) {
        this.success = true;
      } else {
        this.success = false;
      }
      this.loadingPred = false;
    });
    
    switch (this.predictionOption) {
      // case 'global': {
      //   console.log('entro en global');
      //   this.apiService.predictStudentPerformance(this.studentId, targetQuarter).then(res => {
      //     console.log('res', res);
      //     this.predictionResult = res[0][0];
      //     console.log(this.predictionResult);
      //     if (this.predictionResult >= 0.5) {
      //       this.success = true;
      //     } else {
      //       this.success = false;
      //     }
      //     this.loadingPred = false;
      //     this.apiService.predictIndice(this.studentId, targetQuarter).then(res2 => {
      //       console.log('Respuesta modelo indice:', res2);
      //     });
      //   });
      //   break;
      // }
      // case 'custom': {
      //   console.log('entro en custom');
      //   // this.apiService.predictStudentPerformanceByAssigns(this.studentId, targetQuarter).then(res => {
      //   this.apiService.predictPerformanceModel4_V1(this.studentId, targetQuarter).then(res => {
      //     console.log('res', res);
      //     this.predictionResult = res[0][0];
      //     // console.log(this.predictionResult);
      //     if (this.predictionResult >= 0.5) {
      //       this.success = true;
      //     } else {
      //       this.success = false;
      //     }
      //     this.loadingPred = false;
      //   });
      //   break;
      // }
      case 'recomendation': {
        console.log('entro en probatorio');
        this.apiService.predictPerformanceModel5(this.studentId, this.allCombinations).then(res => {
          console.log('res', res);
          this.predictionResult = res;
          // console.log(this.predictionResult);
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

}

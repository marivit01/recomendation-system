import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';

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

  constructor(private formBuilder: FormBuilder, private apiService: ApiService) { }

  ngOnInit() {
    this.createForm();
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
      console.log("all subjects", this.allCombinations);
    });
  }

}

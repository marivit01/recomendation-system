import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  predictionResult;

  constructor(private apiService: ApiService) { }

  ngOnInit() {
  }

  predict() {
    // parameters: X y Y
    const parameters = [];
    this.apiService.predictStudentPerformance(parameters).then( res => {
      this.predictionResult = res;
    });
  }

}

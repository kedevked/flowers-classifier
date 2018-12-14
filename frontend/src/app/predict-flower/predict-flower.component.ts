import { Component, OnInit } from '@angular/core';
import { AppService } from '../app.service';

@Component({
  selector: 'app-predict-flower',
  templateUrl: './predict-flower.component.html',
  styleUrls: ['./predict-flower.component.css']
})
export class PredictFlowerComponent implements OnInit {

  imageSrc: string;
  file: any;
  flowerName: string;
  modelId: string;
  constructor(private appService: AppService) { }

  ngOnInit() {
  }

  onChange(event) {
    this.file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = e => this.imageSrc = reader.result as string;
    reader.readAsDataURL(this.file);
  }

  predict(modelId) {
    console.log(modelId);
    this.appService.predict(this.file, modelId).subscribe(
      (data: {name: string} ) => {
        this.flowerName = data.name;
      });
  }

}

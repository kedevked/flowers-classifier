import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray, FormControl } from '@angular/forms';
import { AppService } from '../app.service';

@Component({
  selector: 'app-upload-model',
  templateUrl: './upload-model.component.html',
  styleUrls: ['./upload-model.component.css']
})
export class UploadModelComponent implements OnInit {
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;
  file: any;
  imageSrc: string;
  thirdFormGroup: FormGroup;
  constructor(
    private _formBuilder: FormBuilder,
    private appService: AppService) { }

  ngOnInit() {
    this.firstFormGroup = this._formBuilder.group({
      featureExtractorCtrl: ['', Validators.required],
      layersCtrl: this._formBuilder.array([
        this.buildLayerCtrl()
      ])
    });
    this.secondFormGroup = this._formBuilder.group({
      emailCtrl: ['']
    });
    this.thirdFormGroup = this._formBuilder.group({
      filename: ['', Validators.required]
    });
  }

  buildLayerCtrl() {
    return this._formBuilder.group({
      nameCtrl: new FormControl('', Validators.required),
      operationCtrl: new FormControl('', Validators.required),
      inputCtrl: new FormControl(null),
      outputCtrl: new FormControl(null),
      dropoutCtrl: new FormControl(null),
      dimCtrl: new FormControl(1)
    });
  }

  addLayer() {
    (this.firstFormGroup.controls.layersCtrl as FormArray).push(this.buildLayerCtrl());
  }

  removeLayer(index: number) {
    (this.firstFormGroup.controls.layersCtrl as FormArray).removeAt(index);
  }

  get lCtrl(): FormArray {
    return this.firstFormGroup.get('layersCtrl') as FormArray;
  }

  onChange(event) {
    this.file = event.target.files[0];
    console.log(this.file);
    this.thirdFormGroup.controls['filename'].setValue(this.file ? this.file.name : '');
    const reader = new FileReader();
    reader.onload = e => this.imageSrc = reader.result as string;
    reader.readAsDataURL(this.file);
  }

  uploadModel() {
    const modelArchitecture = {
      arch: this.firstFormGroup.controls.featureExtractorCtrl.value,
      layers: []
    };
    for (const layercontrol of this.lCtrl.controls) {
      const layer = {
        name: layercontrol.value.nameCtrl,
        type: layercontrol.value.operationCtrl
      };
      switch (layer.type) {
        case 'linear':
          layer['in'] = layercontrol.value.inputCtrl;
          layer['out'] = layercontrol.value.outputCtrl;
          break;
        case 'dropout':
          layer['drop'] = layercontrol.value.dropoutCtrl;
          break;
        case 'logsoft':
          layer['drop'] = layercontrol.value.dimCtrl;
          break;
      }
      modelArchitecture.layers.push(layer);
    }
    const email = this.secondFormGroup.controls.emailCtrl.value;
    this.appService.uploadModel(modelArchitecture, this.file, email).subscribe();
  }

}

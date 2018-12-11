import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PredictFlowerComponent } from './predict-flower/predict-flower.component';
import { UploadModelComponent } from './upload-model/upload-model.component';

const routes: Routes = [
  { path: 'predict-flower', component: PredictFlowerComponent},
  { path: 'upload-model', component: UploadModelComponent},
  { path: '',
    redirectTo: '/predict-flower',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

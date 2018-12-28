import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AppService } from '../app.service';


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent {

  sHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches)
    );
  imageSrc: string;
  file: any;
  flowerName: string;

  constructor(
    private breakpointObserver: BreakpointObserver,
    private appService: AppService
    ) {}

  // move below code later
  onChange(event) {
    this.file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = e => this.imageSrc = reader.result as string;
    reader.readAsDataURL(this.file);
  }

  predict() {
    this.appService.predict(this.file).subscribe(
      (data: {name: string} ) => {
        this.flowerName = data.name;
      }
    );
  }


}

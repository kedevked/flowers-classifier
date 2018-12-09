import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictFlowerComponent } from './predict-flower.component';

describe('PredictFlowerComponent', () => {
  let component: PredictFlowerComponent;
  let fixture: ComponentFixture<PredictFlowerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PredictFlowerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictFlowerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

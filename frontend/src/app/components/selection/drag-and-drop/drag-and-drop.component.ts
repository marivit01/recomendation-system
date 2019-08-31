import { Component, OnInit, Input, Output, EventEmitter, OnChanges } from '@angular/core';
import { CdkDragDrop, moveItemInArray, transferArrayItem } from '@angular/cdk/drag-drop';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'drag-and-drop',
  templateUrl: './drag-and-drop.component.html',
  styleUrls: ['./drag-and-drop.component.css']
})
export class DragAndDropComponent implements OnInit, OnChanges {
  @Input() id: string;
  @Input() loading;
  @Output() targetSubjects = new EventEmitter<string[]>();
  @Output() loaded = new EventEmitter<boolean>();

  allSubjects = [];
  // allSignatures = [
  //   'Matemáticas I',
  //   'Matemáticas II',
  //   'Matemáticas III',
  //   'Algoritmos y Programación',
  //   'Arquictectura del computador',
  //   'Organización del computador',
  //   'Inglés IV',
  //   'Inglés V',
  // ];

  // allSubjects = ['FBTCE03', 'FBTMM00', 'FBTHU01', 'FBTIE02', 'BPTQI21', 'BPTMI04', 'FBPIN01'
  //   , 'BPTPI07', 'FBPLI02', 'FBTIN04', 'FGE0000', 'FBPCE04', 'FBPMM02', 'FBTIN05'
  //   , 'FBPIN03', 'FBPIN02', 'FBPLI01', 'FBPCE03', 'FBPMM01', 'FBTHU02', 'FBTSP03'
  //   , 'BPTFI02', 'BPTMI11', 'BPTSP05', 'BPTMI01', 'FBTCE04', 'FBTMM01', 'FGS0000'
  //   , 'FBTIE03', 'BPTFI03', 'BPTMI20', 'BPTFI01', 'BPTQI22', 'BPTMI05', 'BPTMI30'
  //   , 'BPTSP06', 'BPTMI02', 'BPTMI03', 'FPTCS16', 'FPTSP15', 'BPTEN12', 'BPTMI31'
  //   , 'FPTEN23', 'BPTSP03', 'BPTFI04', 'FPTSP14', 'BPTDI01-1', 'FBTIE01', 'FPTSP20'
  //   , 'FPTMI21', 'BPTSP04', 'FPTSP01', 'FPTSP18', 'FPTSP22', 'FPTSP17', 'FPTPI09'
  //   , 'FPTSP11', 'FPTSP04', 'FPTSP02', 'BPTDI01-2', 'FPTSP23', 'FPTSP19', 'FPTSP07'
  //   , 'FPTSP25', 'FPTSP21', 'FPTIS01'];

  // test: Array<{code: string, name: string}> = [
  //   {
  //     code: 'FGE0000',
  //     name: 'Electiva'
  //   },
  //   {
  //     code: 'FBTMM01',
  //     name: 'Mate 1'
  //   }
  // ];

  studentSubjects = [];

  constructor(private apiService: ApiService) { }

  ngOnInit() {
  }

  ngOnChanges(changes) {
    console.log(changes);
    if (this.id) {
      // Se llama la funcion para obtener las materias disponibles por id del estudiante, y guardarla en allSignatures
      this.getAvailableSubjects(this.id);
    }
  }

  getAvailableSubjects(id) {
    this.apiService.getAvailableSubjects(id).then(res => {
      console.log('res', res);
      this.allSubjects = res;
      this.loaded.emit(false);
    });
  }

  drop(event: CdkDragDrop<string[]>) {
    console.log('all init: ', this.allSubjects);
    console.log('student init: ', this.studentSubjects);
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex);
    }

    console.log('all: ', this.allSubjects);
    console.log('student: ', this.studentSubjects);
    this.formatTarget();
  }

  formatTarget() {
    // Se crea un array con los codigos de las materias seleccionadas para el trimestre target, y se emite al componente padre
    const target = [];
    this.studentSubjects.forEach( subject => {
      target.push(subject.code);
    });
    console.log(target);
    this.targetSubjects.emit(target);
  }
}

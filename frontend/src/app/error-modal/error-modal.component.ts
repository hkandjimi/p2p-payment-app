import { Component } from '@angular/core'
import { MdbModalRef } from 'mdb-angular-ui-kit/modal'

@Component({
  selector: 'app-error-modal',
  templateUrl: './error-modal.component.html',
  styleUrls: ['./error-modal.component.scss']
})
export class ErrorModalComponent {

  errorData: any
  modalType: any
  modalTitle: any
  constructor(public modalRef: MdbModalRef<ErrorModalComponent>) {}

}
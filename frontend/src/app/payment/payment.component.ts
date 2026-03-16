import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { PaymentService } from '../payment.service';

import { CommonModule } from '@angular/common';

import { ReactiveFormsModule } from '@angular/forms';
import { MdbModalRef, MdbModalService } from 'mdb-angular-ui-kit/modal'
import { ErrorModalComponent } from '../error-modal/error-modal.component'

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  standalone: true,
  imports: [
    ReactiveFormsModule,CommonModule,
   ]
})

export class PaymentComponent {

  toastType = 'danger'
  modalRef: MdbModalRef<ErrorModalComponent> | null = null

  constructor(
    private fb: FormBuilder,
    private paymentService: PaymentService,
    private modalService: MdbModalService
  ){}

  paymentForm = this.resetForm()
  resetForm(){
    return this.fb.group({
      clientReference:[''], 
      senderAccountNumber:[''], 
      receiverAccountNumber:[''],
      amount:[''],
      currency:[''],
      reference:[''],
  
    });
  }
  submit(){


    // console.log(this.paymentForm.value); //debuging and tracing

    this.paymentService.sendPayment(this.paymentForm.value).subscribe({

      next: (response) => {
    
        //console.log("Success", response)//debuging and tracing
        
        this.modalRef = this.modalService.open(ErrorModalComponent)
        this.modalRef.component.modalType = "success"
        this.modalRef.component.modalTitle = "Complete"
        this.modalRef.component.errorData = response
        this.paymentForm.reset()
    
      },
      error: (err) => {
        //console.log(err)  //debuging and tracing
        this.modalRef = this.modalService.open(ErrorModalComponent)
        this.modalRef.component.modalType = "danger"
        this.modalRef.component.modalTitle = "Error"
        this.modalRef.component.errorData = err

      }
    
    })
  }

  // showToast(message: string, type: string = 'error') {
  
  //   this.toastMessage = message
  //   this.toastType = type
  //   this.toastVisible = true
  
  //   setTimeout(() => {
  //     this.toastVisible = false
  //   }, 8000)
  
  // }

}

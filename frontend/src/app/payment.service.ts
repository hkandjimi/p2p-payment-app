import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })

export class PaymentService {

  private API = 'http://localhost:8000/api/p2p-payment';

  constructor(private http: HttpClient) {}

  sendPayment(data:any): Observable<any> {
    data["clientReference"] = this.generateTransactionId();
    //remove columns without data from request
    for (let key in data) {
      if (data[key] == "" || data[key] == null) {
         delete data[key];
      }
    }
    // console.log("Received data:",data); //debuging and tracing
    return this.http.post(this.API, data);
  }
  
  //Function to generate transaction ID, done at frontend 
  generateTransactionId(): string {
    const now = new Date()
    const datePart =
      now.getFullYear().toString() +
      String(now.getMonth() + 1).padStart(2, '0') +
      String(now.getDate()).padStart(2, '0')
  
    const timestampPart = Date.now().toString().slice(-3)
  
    const randomPart = Math.floor(100 + Math.random() * 900).toString()
  
    const uniquePart = (timestampPart + randomPart).slice(0, 5)
    //Transaction id format : REF-YYYYMMDD-XXXXX, with XXXXX making up a unique number that combines milliseconds of the current timestampt and a random number between 100 and 900
    return `REF-${datePart}-${uniquePart}`
  }
}
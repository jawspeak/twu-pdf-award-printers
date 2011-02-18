#!/usr/bin/python2.4
# -*- coding: latin-1 -*-
import sys

# has dependencies on reportlab, and pil
# api docs here: http://www.reportlab.com/apis/reportlab/2.4/pdfgen.html#
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors


class AwardPrinter:
  def __init__(self, output_filename, background_image, page_renderer):
    self.background_image = background_image
    self.page_renderer = page_renderer
    self.pdf = Canvas(output_filename, pagesize = A4)        
  
  def draw(self, students):
    for student in students:
        self._draw_page(student)
    self.pdf.save()    
  
  def _draw_page(self, student):
    self.pdf.setFillColor(colors.black)
    # export the image as a higter resolution image 1280x920 recommended, which is then reduced 
    # in size to have a higher resolution for printing
    self.pdf.drawImage(self.background_image, .1 * inch, .3 * inch, width=580, height=800, preserveAspectRatio=True)
    self.pdf.rotate(270)
    self.page_renderer(self, student)
    self.pdf.showPage()    
      
  def _draw_award(self, student):
    name = student.split(',')[0].strip()
    award = student.split(',')[1].strip()
    self.pdf.setFont("Helvetica", 28)    
    self.pdf.drawCentredString(-5.4 * inch, 4.5 * inch, name.encode('latin-1'))
    self.pdf.setFont("Helvetica", 18)
    self.pdf.drawCentredString(-5.4 * inch, 3.5 * inch, award)
    
  def _draw_certificate(self, student):
    name = student.split(',')[0].strip()    
    self.pdf.setFont("Helvetica", 32)
    self.pdf.drawCentredString(-5.75 * inch, 5.5 * inch, name.encode('latin-1'))

  
def main():                
  print sys.argv
  if len(sys.argv) != 2:
    die()
  if sys.argv[1] == 'awards':
    printer = AwardPrinter('Graduation_certs_rendered.pdf', 'backgrounds/TWUCertificate_90.jpg', AwardPrinter._draw_certificate)  
    printer.draw(open('students.txt').readlines())  
  elif sys.argv[1] == 'graduation':
    printer = AwardPrinter('Awards_rendered.pdf', 'backgrounds/award_certificate_90.jpg', AwardPrinter._draw_award)
    printer.draw(open('students.txt').readlines())

def die():
  print ("usage: python %s [awards|graduation]") % __file__
  exit(1)

if __name__ == '__main__':
  main()
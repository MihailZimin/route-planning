#include "mainwindow.h"

#include "./ui_mainwindow.h"
#include "data.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
  ui->setupUi(this);

  QVector<double> x(N), y(N);  // initialize with entries 0..100
  for (int i = 0; i < N; ++i) {
    x[i] = i;
    y[i] = array[i];
  }
  // create graph and assign data to it:
  ui->plot->addGraph();
  ui->plot->graph(0)->setData(x, y);
  // give the axes some labels:
  ui->plot->xAxis->setLabel("x");
  ui->plot->yAxis->setLabel("y");
  // set axes ranges, so we see all data:
  ui->plot->xAxis->setRange(0, 9);
  ui->plot->yAxis->setRange(0, 4);
  ui->plot->replot();
}

MainWindow::~MainWindow() { delete ui; }

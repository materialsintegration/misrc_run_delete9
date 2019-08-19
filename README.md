このリポジトリにはMIシステムで実行したランのうち、異常終了（run_status = 99）または、起動失敗（run_status=9）のランを論理削除するpythonスクリプトが格納されています。

## 概要
MIシステムのワークフロー実行時、特にAPIを使用して実行した場合に、時に起動失敗を起こすことがある。原因はさまざまで特定できていない。このため、自動実行中に大量に起動失敗が発生することがある。かたや異常終了するワークフローがある。
原因はさまざまで、こちらは主にワークフローの堅牢性に問題がある場合がある。こちらも自動実行して大量に異常終了ランを発生させる可能性がある。これらのステータスのランはラン一覧で意味をなさないため、削除したくなることがある。
または定期的にラン一覧をクリーンアップする目的などで削除することもあると思われる。他方、現在用意されているAPIでは大量に論理削除を行えるものはない。このために当スクリプトを整備した。

## システム要件
* python  
  2.7または3.x

* 必要パッケージ
  + mysql-connector-python

* 実行場所
  + MIシステムapdbサーバーのmysqlへ接続できる場所

## 使用方法
```python
$ python delete_run.py <workflow id>
```

workflow id はsite_id（0詰めなし） + workflow_idとする。  
例：
デザイナー上で、「W000020000000197」とあれば、指定は「20000000197」とする。

## 補足
* 実行毎にログファイルが作成される。
  * ログファイルには、ラン番号と内部ランIDが記録される。
* 対象DBとテーブルは、workflow.runである。
* 削除は論理削除で、DBには、deletedに１が、deletion_idにcreatorと同じIDが、deletion_timeに実行時に取得したタイムスタンプが格納される。
* 対象となるworkflow idおよび条件に合致するランが無い場合は、実行されない。

以上
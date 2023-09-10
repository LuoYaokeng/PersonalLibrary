<script setup>
import axios from 'axios'
import { reactive, ref, onMounted } from "vue";
import { ElMessageBox } from 'element-plus';

const books = reactive([])

const getBooks = () => {
  axios.get(`http://127.0.0.1:5000/books`).then(res => {
    books.splice(0, books.length)
    books.push(...res.data.results)
    console.log('更新数据')
  })
}

const value = ref('')
const options = [
  {
    value: 'luoyaokeng',
    label: '铿',
  },
  {
    value: 'chenyuyan',
    label: '妍',
  },
]

const defaultTime = new Date(2000, 1, 1, 12, 0, 0)

const shortcuts = [
  {
    text: 'Today',
    value: new Date(),
  },
  {
    text: 'Yesterday',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24)
      return date
    },
  },
  {
    text: 'A week ago',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
      return date
    },
  },
]

// 页面渲染之后添加数据
onMounted(() => {
  getBooks()
})

// 删除数据
const handleDelete = (index, scope) => {
  console.log
  axios.delete(`http://127.0.0.1:5000/books/${scope.book_id}`).then(() => {
    getBooks()
  })
}

const add_dialog_visible = ref(false)
const ruleFormRef = ref()
const book_form = reactive({
  book_id: "",
  book_title: "",
  book_author: "",
  book_borrower_id: "",
  book_borrow_date: "",
  book_return_date: "",
  book_status: ""
})


const submitForm = (formEl) => {
  console.log(formEl);
  axios.post(`http://127.0.0.1:5000/books`, book_form).then(() => {
    add_dialog_visible.value = false
    formEl.resetFields()
    getBooks()
  })
}
// 重置表单
const resetForm = (formEl) => {
  formEl.resetFields()
}

// 关闭弹窗前确认
const handleClose = (done) => {
  ElMessageBox.confirm('确认关闭？')
    .then(() => {
      done();
    })
    .catch(() => {

    })
}

// 编辑表单
const editFormRef = ref()
const edit_dialog_visible = ref(false)
const handleEdit = (index, scope) => {
  for(let key in scope){
    book_form[key] = scope[key]
  }
  edit_dialog_visible.value = true
}

// 编辑提交按钮
const submitEditForm = (formEl)=>{
  axios.put(`http://127.0.0.1:5000/books/${book_form.book_id}`,book_form).then((res) =>{
    formEl.resetFields()
    edit_dialog_visible.value = false
    getBooks()
  })
}



</script>

<template>
  <div style="margin:0 auto;width:50%;">
    <h1 style="text-align:center">图书管理系统</h1>
    <!-- 添加图书按钮 -->
    <el-button type="primary" @click="add_dialog_visible = true" size="small">添加图书</el-button>
    <!-- 数据表格 -->
    <el-table :data="books" style="margin:20px auto">
      <el-table-column label="编号" prop="book_id" />
      <el-table-column label="书名" prop="book_title" />
      <el-table-column label="作者" prop="book_author" />
      <el-table-column label="借阅人" prop="book_borrower_id" />
      <el-table-column label="借阅日期" prop="book_borrow_date" />
      <el-table-column label="应还日期" prop="book_return_date" />
      <el-table-column label="状态" prop="book_status" />
      <el-table-column align="right" label="操作" width="200px">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
            编辑
          </el-button>
          <el-button 
            size="small" 
            type="danger" 
            @click="handleDelete(scope.$index, scope.row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>


  <!-- 添加图书页面 -->
  <el-dialog title="添加图书" v-model="add_dialog_visible" width="30%">
    <el-form 
            ref="ruleFormRef" 
            :model="book_form" 
            status-icon 
            label-width="120px" 
            class="demo-ruleForm"
    >
      <el-form-item label="书名" prop="book_title">
        <el-input v-model="book_form.book_title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="作者" prop="book_author">
        <el-input v-model="book_form.book_author" autocomplete="off" />
      </el-form-item>
      <el-form-item label="借阅人" prop="book_borrower_id">
        <el-select v-model="book_form.book_borrower_id" clearable placeholder="请选择借阅人">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="借阅日期" prop="book_borrow_date">
        <el-date-picker
          v-model="book_form.book_borrow_date"
          type="date"
          placeholder="请选择借书日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          :shortcuts="shortcuts"
        />
      </el-form-item>
      <el-form-item label="应还日期" prop="book_return_date">
        <el-date-picker
          v-model="book_form.book_return_date"
          type="date"
          placeholder="请选择借书日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          :shortcuts="shortcuts"
        />
      </el-form-item>
      <el-form-item label="状态" prop="book_status">
        <el-input v-model="book_form.book_status" autocomplete="off" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)">提交</el-button>
        <el-button @click="resetForm(ruleFormRef)">重置</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>

  <el-dialog
    title = "编辑图书"
    v-model = "edit_dialog_visible"
    width = "30%"
  >
    <el-form
      ref = "editFormRef"
      :model = "book_form"
      status-icon
      label-width = "120px"
      class = "demo-ruleForm"
    >
      <el-form-item label="书名" prop="book_title">
        <el-input v-model="book_form.book_title" autocomplete="off" />
      </el-form-item>
      <el-form-item label="作者" prop="book_author">
        <el-input v-model="book_form.book_author" autocomplete="off" />
      </el-form-item>
      <el-form-item label="借阅人" prop="book_borrower_id">
        <el-select v-model="book_form.book_borrower_id" clearable placeholder="请选择借阅人">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="借阅日期" prop="book_borrow_date">
        <el-date-picker
          v-model="book_form.book_borrow_date"
          type="date"
          placeholder="请选择借书日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          :shortcuts="shortcuts"
        />
      </el-form-item>
      <el-form-item label="应还日期" prop="book_return_date">
        <el-date-picker
          v-model="book_form.book_return_date"
          type="date"
          placeholder="请选择借书日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          :shortcuts="shortcuts"
        />
      </el-form-item>
      <el-form-item label="状态" prop="book_status">
        <el-input v-model="book_form.book_status" autocomplete="off" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitEditForm(editFormRef)">提交</el-button>
        <el-button @click="resetForm(editFormRef)">重置</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<style scoped>

</style>

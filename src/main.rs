fn main() {
    let interpreter = rustpython_vm::Interpreter::with_init(Default::default(), |vm| {
        // vm.add_native_module(
        //     "pyaici.server_native".to_owned(),
        //     Box::new(_aici::make_module),
        // );
        // vm.add_frozen(rustpython_vm::py_freeze!(dir = "Lib"));

        let code = rustpython_vm::py_compile!(
            file = "src/search.py",
            module_name = "search",
            mode = "exec"
        );
        // let empty =
        //     rustpython_vm::py_compile!(source = "# nothing", module_name = "pyaici", mode = "exec");
        // let frozen_vec = vec![
        //     (
        //         "pyaici",
        //         rustpython_vm::frozen::FrozenModule {
        //             code: empty,
        //             package: true,
        //         },
        //     ),
        //     (
        //         "pyaici.server",
        //         rustpython_vm::frozen::FrozenModule {
        //             code,
        //             package: true,
        //         },
        //     ),
        // ];
        // vm.add_frozen(frozen_vec.into_iter());
    });
    interpreter.enter(|vm| {
        let scope = vm.new_scope_with_builtins();

        let r = vm
            .compile(
                &source,
                rustpython_vm::compiler::Mode::Exec,
                "<arg>".to_owned(),
            )
            .map_err(|err| vm.new_syntax_error(&err, Some(&source)))
            .and_then(|code_obj| vm.run_code_obj(code_obj, scope));

        match r {
            Ok(res) => {
                println!("{res:?");
                // make sure the callback is registered
                // let _ = get_cb_obj();
            }
            Err(e) => {
                vm.print_exception(e.clone());
                panic!("Python Exception: {e:?}");
            }
        }
    });
}
